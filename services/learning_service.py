def get_approved_learning_examples(connection, company_id):

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        customer_message,
        approved_reply,
        intent
    FROM ai_learning
    WHERE
        company_id=%s
        AND review_status='Approved'
    ORDER BY id DESC
    """

    cursor.execute(
        query,
        (company_id,)
    )

    examples = cursor.fetchall()

    cursor.close()

    return examples