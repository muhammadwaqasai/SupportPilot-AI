from openai import OpenAI
from dotenv import load_dotenv
import os
from knowledge_reader import load_knowledge

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=60.0
)


def generate_reply(message):

    company_info = load_knowledge()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a professional AI Customer Support Agent.

Use the following company information to answer customer questions.

Company Information:

{company_info}

Rules:
- Answer using the company information whenever possible.
- If the answer is not in the company information, politely say you don't have that information and ask the customer to contact support.
- Be polite, professional, and concise.
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content