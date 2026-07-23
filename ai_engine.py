from openai import OpenAI
from dotenv import load_dotenv
from rag.retriever import search_knowledge
import os
import json


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=120.0
)




def analyze_customer_message(
        message,
        history=None,
        company_id="company_1"
):


    # RAG: Retrieve company-specific knowledge

    company_info = search_knowledge(
        message,
        company_id
    )



    if history is None:

        history = []



    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        response_format={
            "type": "json_object"
        },


        messages=[

            {

                "role": "system",

                "content": f"""

You are an advanced AI Customer Support Copilot.

Your job is to analyze customer messages and help a support team.


Use the retrieved company knowledge below.


Company Knowledge:

{company_info}



Previous Customer History:

{history}



Return ONLY valid JSON.



Required JSON format:


{{
 "reply": "",
 "summary": "",
 "intent": "",
 "department": "",
 "priority": "",
 "sentiment": "",
 "risk_level": "",
 "recommended_action": "",
 "escalation": "",
 "confidence_score": 0
}}



Rules:


1. Reply:

Write a polite professional response to the customer.

Use company knowledge when available.



2. Summary:

Give a short one sentence summary of the issue.



3. Intent:

Identify customer purpose.

Examples:

- Order Issue
- Refund Request
- Product Inquiry
- Complaint
- Technical Support
- General Question



4. Department:

Choose:

- Sales
- Billing
- Shipping
- Technical Support
- Customer Service



5. Priority:

Only:

- Low
- Medium
- High



6. Sentiment:

Only:

- Positive
- Neutral
- Negative



7. Risk Level:

Choose ONLY one:

- Low
- Medium
- High


Risk Level Rules:

High:
- Customer threatens legal action.
- Customer threatens public complaints or social media.
- Customer demands an immediate refund aggressively.
- Customer uses abusive or offensive language.
- Customer reports a serious financial or security issue.
- Customer repeatedly reports unresolved issues.

Medium:
- Refund requests.
- Product not working.
- Shipping delays.
- Billing issues.
- General complaints.

Low:
- Product inquiries.
- Order status questions.
- General information requests.


8. Recommended Action:

Suggest the best next action for the support team.


9. Escalation:

Choose ONLY:

- Yes
- No


Escalation Rules:

Return "Yes" if the customer:

- asks to speak with a manager
- threatens legal action
- threatens negative reviews or social media exposure
- demands an urgent refund aggressively
- is extremely angry
- uses abusive language
- has contacted support multiple times without resolution

Otherwise return "No".



10. Confidence Score:

Give confidence from 0 to 100.



If company knowledge does not contain the answer:

- Do not invent information.
- Tell the customer support team will assist them.

"""

            },


            {

                "role": "user",

                "content": message

            }

        ]

    )



    result = response.choices[0].message.content



    return json.loads(result)