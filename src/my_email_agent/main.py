import os
from composio  import Composio
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
USER_EMAIL = os.getenv("USER_EMAIL")
GMAIL_AUTH_CONFIG_ID = os.getenv("COMPOSIO_GMAIL_CONNECTION_ID")


# Connect Gmail account
connection_request = composio.connected_accounts.initiate(
    user_id=USER_EMAIL,
    auth_config_id=GMAIL_AUTH_CONFIG_ID,
)

# Redirect user to OAuth flow
redirect_url = connection_request.redirect_url
print(f"Visit this URL to authorize: {redirect_url}")

# Wait for connection
connected_account = connection_request.wait_for_connection()
print("✅ Gmail account connected!")

# Get Gmail tools
tools = composio.tools.get(user_id=USER_EMAIL, tools=["GMAIL_SEND_EMAIL"])

# Generate email content using OpenAI
# Generate email content using Groq
response = groq_client.chat.completions.create(
     model="llama-3.3-70b-versatile",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": (
                f"Send an email to {USER_EMAIL} with subject 'Hello from composio 👋🏻' "
                "and body 'Congratulations on sending your first email using AI Agents and Composio!'"
            ),
        },
    ],
)


# Execute the tool call
result = composio.provider.handle_tool_calls(response=response, user_id=USER_EMAIL)
print(result)
print("✅ Email sent successfully!")

# Create a trigger to monitor new emails
trigger = composio.triggers.create(
    user_id=USER_EMAIL,
    slug="GMAIL_NEW_GMAIL_MESSAGE",
    trigger_config={"labelIds": "INBOX", "userId": "me", "interval": 60},
)
print(f"✅ Trigger created successfully. Trigger Id: {trigger.trigger_id}")

# Subscribe to trigger events
subscription = composio.triggers.subscribe()

@subscription.handle(trigger_id=trigger.trigger_id)
def handle_gmail_event(data):
    print("New Gmail Event:", data)
