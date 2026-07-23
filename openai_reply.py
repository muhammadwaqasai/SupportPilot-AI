from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_ai_reply(message):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
You are a professional customer support assistant.

Reply politely and professionally to this customer.

Customer Message:
{message}
"""
    )

    return response.output_text