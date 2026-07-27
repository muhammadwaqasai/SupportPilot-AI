import json

from openai_reply import client

MODEL = "gpt-4.1-mini"


def generate_ai_business_report(stats):

    prompt = f"""
You are an expert business consultant.

Analyze these customer support statistics.

Statistics:

{json.dumps(stats, indent=2)}

Return ONLY valid JSON.

{{
    "health_score": 0,
    "business_health": "",
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "recommendations": [],
    "urgent_action": ""
}}

Rules:

- Health score between 0 and 100
- Be realistic
- Think like a CEO advisor
- Recommendations must be practical
- Weaknesses should identify business risks
"""
    response = client.chat.completions.create(

        model=MODEL,

        messages=[

            {
                "role": "system",
                "content": "You are an experienced business consultant."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        response_format={"type": "json_object"}

    )


    report = json.loads(
        response.choices[0].message.content
    )

    return report