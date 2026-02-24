import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot Configuration"""

    PORT = int(os.environ.get("PORT", 3978))  # Use Azure's PORT or default to 3978 for local
    APP_ID = os.environ.get("BOT_ID", "")
    APP_PASSWORD = os.environ.get("BOT_PASSWORD", "")  # Bot secret/password (empty for managed identity)
    APP_TYPE = os.environ.get("BOT_TYPE", "MultiTenant")  # UserAssignedMsi or MultiTenant
    APP_TENANTID = os.environ.get("BOT_TENANT_ID", "")
    # For Managed Identity
    CLIENT_ID = os.environ.get("CLIENT_ID", "")  # Managed Identity Client ID
    TENANT_ID = os.environ.get("TENANT_ID", "")  # Managed Identity Tenant ID
    AZURE_OPENAI_API_KEY = os.environ.get("SECRET_AZURE_OPENAI_API_KEY") or os.environ.get("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_MODEL_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "")
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"] # Azure OpenAI endpoint
