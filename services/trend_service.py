import json

from openai_reply import client


def analyze_trends(data):

    prompt = f"""
You are a business intelligence analyst.

Analyze these customer support trends:

{json.dumps(data, indent=2, default=str)}


Return ONLY JSON:

{{
    "trend_summary": "",
    "sentiment_change": "",
    "main_causes": [],
    "business_risk": "",
    "recommended_actions": []
}}

Focus on:
- customer satisfaction changes
- repeated problems
- operational risks
- useful business actions
"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content": "You analyze business trends."
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