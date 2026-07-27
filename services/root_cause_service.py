import json

from openai_reply import client


MODEL = "gpt-4.1-mini"


def analyze_root_causes(tickets):

    prompt = f"""
You are a senior business analyst.

Analyze these customer support tickets.

Tickets:

{json.dumps(tickets, indent=2)}


Return ONLY valid JSON:

{{
    "main_problems": [],
    "common_complaints": [],
    "affected_departments": [],
    "customer_patterns": [],
    "business_risks": [],
    "recommended_actions": []
}}


Rules:

- Find repeated problems
- Identify patterns
- Explain business impact
- Give practical actions
- Do not give generic advice
"""


    response = client.chat.completions.create(

        model=MODEL,

        messages=[

            {
                "role": "system",
                "content": "You are an expert customer experience analyst."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        response_format={
            "type": "json_object"
        }

    )


    return json.loads(
        response.choices[0].message.content
    )