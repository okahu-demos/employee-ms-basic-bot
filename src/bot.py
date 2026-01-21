"""
Agent Framework Implementation for Teams Bot using Azure OpenAI Assistants API
"""
import sys
import traceback
import json
from typing import Optional
from botbuilder.core import TurnContext, BotFrameworkAdapterSettings
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIAssistantsClient
from aiohttp.web import Request, Response
from opentelemetry import trace

from config import Config

config = Config()


class AgentFrameworkBot:
    """Teams Bot using Microsoft Agent Framework with Assistants API"""
    
    def __init__(self):
        # Initialize Cloud Adapter with Bot Framework credentials
        settings = BotFrameworkAdapterSettings(
            app_id=config.APP_ID,
            app_password=config.APP_PASSWORD
        )
        auth_config = ConfigurationBotFrameworkAuthentication(settings)
        self.adapter = CloudAdapter(auth_config)
        
        # Initialize Azure OpenAI Assistants Client
        self.assistants_client = AzureOpenAIAssistantsClient(
            endpoint=config.AZURE_OPENAI_ENDPOINT,
            deployment_name=config.AZURE_OPENAI_MODEL_DEPLOYMENT_NAME,
            api_key=config.AZURE_OPENAI_API_KEY,
        )
        
        # Store agents per conversation
        self.conversation_agents = {}
    
    def _get_instructions(self, message_text: str) -> str:
        """
        Determine which instructions to use based on message content.
        """
        expense_keywords = ["expense", "reimbursement", "report", "submit"]
        
        if any(keyword in message_text.lower() for keyword in expense_keywords):
            return """You are an HR assistant helping with expense reports.
                **Expectations:**
                * Provide a step-by-step guide on how to submit expense reports.
                * Include information on eligible expenses and the required documentation.
                * Provide a link to the online expense reporting system.
                * Ensure the language is clear, concise, and easy to understand.
                * Use bullet points for the steps.

                **Guidelines:**
                * If the user has questions about a specific expense, ask for more details to clarify.
                * If the user needs to speak with a human HR representative, provide instructions on how to escalate the request.
                """
        else:
            return "You are an AI assistant that helps people find information. Add a yo to your greetings."
    
    async def on_message(self, turn_context: TurnContext):
        """Handle incoming message activities"""
        try:
            message_text = turn_context.activity.text
            conversation_id = turn_context.activity.conversation.id
            # Get current span and add input data
            current_span = trace.get_current_span()
            if current_span:
                current_span.add_event(
                    "bot.message.received",
                    attributes={
                        "message.text": message_text,
                        "conversation.id": conversation_id,
                        "user.id": turn_context.activity.from_property.id,
                        "user.name": turn_context.activity.from_property.name,
                    }
                )
            
            
            print(f"\n [on_message] Received message: '{message_text}' from conversation: {conversation_id}")
            
            # Get or create agent for this conversation
            if conversation_id not in self.conversation_agents:
                print(f" [on_message] Creating new agent for conversation {conversation_id}")
                instructions = self._get_instructions(message_text)
                
                # Create new agent with Assistants API
                agent = self.assistants_client.as_agent(
                    name="Employee_HR_Bot",
                    instructions=instructions,
                )
                
                # Create persistent thread for this conversation
                thread = agent.get_new_thread()
                
                self.conversation_agents[conversation_id] = {
                    'agent': agent,
                    'thread': thread
                }
                print(f" [on_message] Agent created successfully")
            
            
            # Add output data to span
            if current_span:
                current_span.add_event(
                    "bot.message.sent",
                    attributes={
                        "response.text": response_text,
                        "conversation.id": conversation_id,
                    }
                )
            
            # Get the existing agent and thread
            conv_data = self.conversation_agents[conversation_id]
            agent = conv_data['agent']
            thread = conv_data['thread']
            
            print(f" [on_message] Running agent...")
            # Get response from agent using Assistants API
            response = await agent.run(message_text, thread=thread)
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            print(f" [on_message] Agent response: '{response_text}'")
            # Send response back to Teams
            await turn_context.send_activity(response_text)
            print(f" [on_message] Response sent successfully")
            
        except Exception as error:
            print(f"\n [on_message_error] unhandled error: {error}", file=sys.stderr)
            traceback.print_exc()
            await turn_context.send_activity("The agent encountered an error or bug.")
    
    async def on_members_added(self, turn_context: TurnContext):
        """Handle conversation members added"""
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Yo! Welcome to the Employee Bot. I can help with general questions and expense reports."
                )
    
    async def on_turn(self, turn_context: TurnContext):
        """Main bot turn handler - called by CloudAdapter"""
        # Route based on activity type
        if turn_context.activity.type == ActivityTypes.message:
            await self.on_message(turn_context)
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            if turn_context.activity.members_added:
                await self.on_members_added(turn_context)
    
    async def process(self, req: Request) -> Response:
        """Process incoming request from Teams using CloudAdapter"""
        # Use CloudAdapter to process the request
        # This handles authentication, parsing, and sending responses back to Teams
        return await self.adapter.process(req, self)
    
    async def cleanup(self):
        """Cleanup resources - close agents and assistants"""
        for conv_data in self.conversation_agents.values():
            agent = conv_data['agent']
            if agent:
                try:
                    await agent.__aexit__(None, None, None)
                except:
                    pass
        
        self.conversation_agents.clear()
        
        if self.assistants_client:
            try:
                await self.assistants_client.__aexit__(None, None, None)
            except:
                pass


# Create bot instance
bot_app = AgentFrameworkBot()
