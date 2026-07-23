def generate_learning_analytics(learning_examples):

    total_examples = len(learning_examples)


    approved_examples = sum(
        1 for item in learning_examples
        if item.get("review_status") == "Approved"
    )


    rejected_examples = sum(
        1 for item in learning_examples
        if item.get("review_status") == "Rejected"
    )


    pending_examples = sum(
        1 for item in learning_examples
        if item.get("review_status") == "Pending"
    )


    company_versions = {}


    for item in learning_examples:

        company = item.get("company_id")

        if company:
            company_versions[company] = (
                company_versions.get(company, 0) + 1
            )


    return {

        "total_examples": total_examples,

        "approved_examples": approved_examples,

        "rejected_examples": rejected_examples,

        "pending_examples": pending_examples,

        "company_distribution": company_versions

    }