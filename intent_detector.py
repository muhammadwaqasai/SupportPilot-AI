from openai import OpenAI
from dotenv import load_dotenv
import os

from knowledge_reader import load_knowledge


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=60.0
)



def analyze_customer_message(message, customer_history=None):


    company_info = load_knowledge()


    history_text = "No previous customer history available."


    if customer_history:


        history_text = ""


        for item in customer_history:

            history_text += f"""
Previous Issue:
{item['message']}

Previous AI Reply:
{item['ai_reply']}

Intent:
{item['intent']}

Department:
{item['department']}

Priority:
{item['priority']}

Status:
{item['status']}

-------------------
"""



    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {

                "role":"system",

                "content":f"""

You are an advanced AI Customer Support Agent.

Company Information:

{company_info}


Customer Previous History:

{history_text}


Analyze the new customer message.


Return ONLY this format:


Reply:
(write professional customer reply)


Intent:
Department:
Priority:
Sentiment:

Summary:

Recommended_Action:

Risk_Level:

Escalation:

Confidence_Score:


Rules:

Priority:
Low, Medium, or High

Risk_Level:
Low, Medium, or High

Escalation:
Yes or No

Confidence_Score:
number between 0 and 100

Use previous customer history when creating the reply.

"""

            },


            {

                "role":"user",

                "content":message

            }

        ]

    )



    result = response.choices[0].message.content



    data = {}



    lines = result.split("\n")



    current_key = None



    for line in lines:


        if ":" in line:


            key,value = line.split(":",1)

            current_key = key.strip().lower()

            data[current_key] = value.strip()


        elif current_key:

            data[current_key] += " " + line.strip()




    return {


        "reply": data.get("reply",""),

        "intent": data.get("intent",""),

        "department": data.get("department",""),

        "priority": data.get("priority",""),

        "sentiment": data.get("sentiment",""),


        "summary": data.get("summary",""),

        "recommended_action": data.get("recommended_action",""),


        "risk_level": data.get("risk_level",""),


        "escalation": data.get("escalation",""),


        "confidence_score": data.get("confidence_score","0")

    }