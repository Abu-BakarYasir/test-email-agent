import os
from dotenv import load_dotenv

load_dotenv()

COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USER_EMAIL = os.getenv("USER_EMAIL")
GMAIL_AUTH_CONFIG_ID = os.getenv("COMPOSIO_GMAIL_CONNECTION_ID")
