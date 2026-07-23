from mysql_operations import connect_database
from intent_detector import detect_intent


# Connect database
connection = connect_database()

cursor = connection.cursor(dictionary=True)


# Get customers with missing AI analysis
query = """
SELECT id, message 
FROM customers
WHERE intent IS NULL 
OR department IS NULL
OR intent = 'None'
"""

cursor.execute(query)

customers = cursor.fetchall()


print(f"Found {len(customers)} customers to update.")


for customer in customers:

    customer_id = customer["id"]
    message = customer["message"]


    print("\nAnalyzing:")
    print(message)


    # AI detection
    result = detect_intent(message)


    print(result)


    update_query = """
    UPDATE customers
    SET intent=%s,
        department=%s,
        priority=%s,
        sentiment=%s
    WHERE id=%s
    """


    values = (
        result["intent"],
        result["department"],
        result["priority"],
        result["sentiment"],
        customer_id
    )


    cursor.execute(update_query, values)

    connection.commit()


print("\nAll customers updated successfully!")


cursor.close()
connection.close()