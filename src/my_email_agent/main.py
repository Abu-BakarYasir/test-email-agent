import os
from dotenv import load_dotenv
from composio import Composio
from my_email_agent.crew import MyEmailAgentCrew
import time
import json

load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
USER_EMAIL = os.getenv("USER_EMAIL")
GMAIL_AUTH_CONFIG_ID = os.getenv("COMPOSIO_GMAIL_CONNECTION_ID")

# Create a trigger to monitor new emails every 10 seconds
trigger = composio.triggers.create(
    user_id=USER_EMAIL,
    slug="GMAIL_NEW_GMAIL_MESSAGE",
    trigger_config={"labelIds": "INBOX", "userId": "me", "interval": 10},
)
print(f"✅ Trigger created successfully. Trigger Id: {trigger.trigger_id}")

# Subscribe to trigger events
subscription = composio.triggers.subscribe()

@subscription.handle(trigger_id=trigger.trigger_id)
def handle_new_email(data):
    print("Raw Event Data:", json.dumps(data, indent=2))  # Log raw data for debugging
    thread_id = data.get('payload', {}).get('threadId', None)
    if not thread_id:
        print("No thread ID found in event data. Checking raw data:", data)
        return
    
    email_crew = MyEmailAgentCrew()
    result = email_crew.crew().kickoff(inputs={"thread_id": thread_id})
    
    print("Full Email Thread Context:")
    print(result)

# Keep the script running to listen for events
print("Listening for new email events... Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)  # Keep the script alive and allow event processing
except KeyboardInterrupt:
    print("Stopped by user.")