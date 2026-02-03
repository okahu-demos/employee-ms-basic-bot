"""Tests for bot using TraceAssertion fluent API"""
import pytest
from asyncio import sleep
from monocle_test_tools import TraceAssertion
from dotenv import load_dotenv
load_dotenv()


@pytest.mark.asyncio
async def test_expense_report_submission(monocle_trace_asserter: TraceAssertion):
    """Test bot response for expense report submission query"""
    from bot import bot_app
    from botbuilder.schema import Activity, ChannelAccount, ConversationAccount, ActivityTypes
    from botbuilder.core import TurnContext
    from unittest.mock import Mock, AsyncMock
    
    activity = Activity(
        type=ActivityTypes.message,
        text="How do I submit an expense report?",
        channel_id="msteams",
        from_property=ChannelAccount(id="test-user", name="Test User"),
        recipient=ChannelAccount(id="bot-id", name="Bot"),
        conversation=ConversationAccount(id="test-conv", name="Test", conversation_type="personal"),
        channel_data={"tenant": {"id": "test-tenant-id"}}
    )
    
    context = Mock(spec=TurnContext)
    context.activity = activity
    context.send_activity = AsyncMock()
    
    await bot_app.on_message(context)
    await sleep(1)
    
    # Fluent assertions - passing test
    monocle_trace_asserter.called_agent("Employee_HR_Bot").contains_output("expense")


@pytest.mark.asyncio
async def test_hr_policies_query(monocle_trace_asserter: TraceAssertion):
    """Test bot response for HR policies query"""
    from bot import bot_app
    from botbuilder.schema import Activity, ChannelAccount, ConversationAccount, ActivityTypes
    from botbuilder.core import TurnContext
    from unittest.mock import Mock, AsyncMock
    
    activity = Activity(
        type=ActivityTypes.message,
        text="What are the HR policies?",
        channel_id="msteams",
        from_property=ChannelAccount(id="test-user", name="Test User"),
        recipient=ChannelAccount(id="bot-id", name="Bot"),
        conversation=ConversationAccount(id="test-conv", name="Test", conversation_type="personal"),
        channel_data={"tenant": {"id": "test-tenant-id"}}
    )
    
    context = Mock(spec=TurnContext)
    context.activity = activity
    context.send_activity = AsyncMock()
    
    await bot_app.on_message(context)
    await sleep(1)
    
    # Fluent assertions - passing test
    monocle_trace_asserter.called_agent("Employee_HR_Bot").has_input("What are the HR policies?")


@pytest.mark.asyncio
async def test_reimbursement_process(monocle_trace_asserter: TraceAssertion):
    """Test bot response for reimbursement process query"""
    from bot import bot_app
    from botbuilder.schema import Activity, ChannelAccount, ConversationAccount, ActivityTypes
    from botbuilder.core import TurnContext
    from unittest.mock import Mock, AsyncMock
    
    activity = Activity(
        type=ActivityTypes.message,
        text="Tell me about expense reimbursement process",
        channel_id="msteams",
        from_property=ChannelAccount(id="test-user", name="Test User"),
        recipient=ChannelAccount(id="bot-id", name="Bot"),
        conversation=ConversationAccount(id="test-conv", name="Test", conversation_type="personal"),
        channel_data={"tenant": {"id": "test-tenant-id"}}
    )
    
    context = Mock(spec=TurnContext)
    context.activity = activity
    context.send_activity = AsyncMock()
    
    await bot_app.on_message(context)
    await sleep(1)
    
    # Fluent assertions - passing test
    monocle_trace_asserter.called_agent("Employee_HR_Bot").contains_output("reimbursement")


@pytest.mark.asyncio
async def test_agent_invocation_fluent(monocle_trace_asserter: TraceAssertion):
    """Test using fluent assertions - this one will fail silently on wrong agent name"""
    from bot import bot_app
    from botbuilder.schema import Activity, ChannelAccount, ConversationAccount, ActivityTypes
    from botbuilder.core import TurnContext
    from unittest.mock import Mock, AsyncMock
    
    # Create mock turn context
    activity = Activity(
        type=ActivityTypes.message,
        text="What are the HR policies?",
        channel_id="msteams",
        from_property=ChannelAccount(id="test-user", name="Test User"),
        recipient=ChannelAccount(id="bot-id", name="Bot"),
        conversation=ConversationAccount(id="test-conv", name="Test", conversation_type="personal"),
        channel_data={"tenant": {"id": "test-tenant-id"}}
    )
    
    context = Mock(spec=TurnContext)
    context.activity = activity
    context.send_activity = AsyncMock()
    
    # Run bot
    await bot_app.on_message(context)
    await sleep(1)
    
    # Fluent assertions - this will fail because agent name is wrong
    monocle_trace_asserter.called_agent("Wrong_Agent_Name").contains_output("HR policies")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
