def generate_dashboard_analytics(customers):

    total_customers = len(customers)

    high_priority = sum(
        1 for c in customers
        if c.get("priority") == "High"
    )

    negative_sentiment = sum(
        1 for c in customers
        if c.get("sentiment") == "Negative"
    )

    completed_cases = sum(
        1 for c in customers
        if c.get("status") == "Completed"
    )

    ai_solved_cases = sum(
        1 for c in customers
        if c.get("status") == "Completed"
        and c.get("was_edited") in [0, False, "0", None]
    )

    human_review_cases = sum(
        1 for c in customers
        if c.get("status") == "Waiting Review"
    )

    escalation_cases = sum(
        1 for c in customers
        if c.get("escalation") == "Yes"
    )

    high_risk_cases = sum(
        1 for c in customers
        if c.get("risk_level") == "High"
    )

    confidence_values = []

    for c in customers:

        try:
            confidence_values.append(
                float(c.get("confidence_score", 0))
            )
        except:
            pass

    average_confidence = 0

    if confidence_values:

        average_confidence = round(
            sum(confidence_values) /
            len(confidence_values),
            2
        )

    ai_solved_percentage = 0
    human_review_percentage = 0
    escalation_percentage = 0

    if total_customers:

        ai_solved_percentage = round(
            (ai_solved_cases / total_customers) * 100,
            2
        )

        human_review_percentage = round(
            (human_review_cases / total_customers) * 100,
            2
        )

        escalation_percentage = round(
            (escalation_cases / total_customers) * 100,
            2
        )

    priority_data = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    sentiment_data = {
        "Positive": 0,
        "Neutral": 0,
        "Negative": 0
    }

    department_data = {}

    for customer in customers:

        priority = customer.get("priority")

        if priority in priority_data:
            priority_data[priority] += 1

        sentiment = customer.get("sentiment")

        if sentiment in sentiment_data:
            sentiment_data[sentiment] += 1

        department = customer.get("department")

        if department:
            department_data[department] = (
                department_data.get(department, 0) + 1
            )

    return {

        "total_customers": total_customers,

        "high_priority": high_priority,

        "negative_sentiment": negative_sentiment,

        "completed_cases": completed_cases,

        "ai_solved_cases": ai_solved_cases,

        "human_review_cases": human_review_cases,

        "escalation_cases": escalation_cases,

        "high_risk_cases": high_risk_cases,

        "average_confidence": average_confidence,

        "ai_solved_percentage": ai_solved_percentage,

        "human_review_percentage": human_review_percentage,

        "escalation_percentage": escalation_percentage,

        "priority_data": priority_data,

        "sentiment_data": sentiment_data,

        "department_data": department_data

    }