"""Pytest configuration and fixtures"""
import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# # Enable Monocle Tracing for tests
# from monocle_apptrace import setup_monocle_telemetry
# setup_monocle_telemetry(workflow_name='employee-ms-basic-bot-tests', monocle_exporters_list='file,okahu')


@pytest.fixture
def real_config():
    """Real configuration settings from environment"""
    from dotenv import load_dotenv
    load_dotenv()
    return {
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
        "AZURE_OPENAI_MODEL_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "CLIENT_ID": os.getenv("CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("CLIENT_SECRET"),
        "APP_ID": os.getenv("CLIENT_ID"),
        "APP_PASSWORD": os.getenv("CLIENT_SECRET"),
        "OKAHU_API_KEY": os.getenv("OKAHU_API_KEY"),
        "OKAHU_INGESTION_ENDPOINT": os.getenv("OKAHU_INGESTION_ENDPOINT"),
    }         