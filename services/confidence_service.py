def evaluate_ticket(
        confidence_score,
        escalation,
        risk_level
):


    # Escalation always requires human review

    if escalation == "Yes":

        return {
            "auto_send": False,
            "status": "Waiting Review",
            "reason": "Escalation required"
        }



    # Low confidence requires human review

    if confidence_score < 80:

        return {
            "auto_send": False,
            "status": "Waiting Review",
            "reason": "Low confidence"
        }




    # High risk requires human review

    if risk_level == "High":

        return {
            "auto_send": False,
            "status": "Waiting Review",
            "reason": "High risk ticket"
        }




    # Safe case

    return {
        "auto_send": True,
        "status": "Completed",
        "reason": "High confidence safe response"
    }