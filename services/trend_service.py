import json

from openai_reply import client


def analyze_trends(data):

    # Limit data sent to AI to avoid Render timeout and huge requests
    if len(data) > 20:
        data = data[:20]

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

    try:

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
            },

            timeout=30
        )

        return json.loads(
            response.choices[0].message.content
        )

    except Exception as e:

        return {
            "trend_summary": "AI analysis temporarily unavailable.",
            "sentiment_change": "",
            "main_causes": [],
            "business_risk": str(e),
            "recommended_actions": [
                "Try generating insights again later."
            ]
        }