def generate_business_advice(stats):

    total = stats["total"]

    negative = stats["sentiment"]["negative"]

    positive = stats["sentiment"]["positive"]

    escalated = stats["escalated"]

    high_priority = stats["priority"].get(
        "High",
        0
    )


    advice = []


    # Business health

    if total == 0:

        health = "No Data"

    elif negative > positive:

        health = "Needs Attention"

    else:

        health = "Healthy"



    # Detect problems


    if negative > 5:

        advice.append(
            "Many customers show negative sentiment. Review complaint reasons."
        )


    if high_priority > 5:

        advice.append(
            "High priority tickets are increasing. Improve response time."
        )


    if escalated > 3:

        advice.append(
            "Several tickets are escalated. Check unresolved customer issues."
        )


    if not advice:

        advice.append(
            "Customer support performance looks stable."
        )



    # Recommendations

    recommendations = [

        "Analyze repeated customer complaints.",

        "Improve response speed for high priority tickets.",

        "Train support staff using AI insights."

    ]



    return {

        "health": health,

        "issues": advice,

        "recommendations": recommendations

    }