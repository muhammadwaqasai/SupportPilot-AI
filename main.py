from mysql_operations import (
    connect_database,
    insert_customer,
    customer_exists,
    update_customer
)

from ai_reply import generate_reply
from intent_detector import detect_intent
from email_sender import send_email
import pandas as pd


# Connect to MySQL
connection = connect_database()

if connection.is_connected():
    print("Database Connected Successfully!")


# Read customer data from CSV
customers = pd.read_csv("customers.csv")


# Process each customer
for index, row in customers.iterrows():

    name = row["customer_name"]
    email = row["email"]
    message = row["message"]


    # Analyze customer message using AI
    analysis = detect_intent(message)

    intent = analysis["intent"]
    department = analysis["department"]
    priority = analysis["priority"]
    sentiment = analysis["sentiment"]


    # Generate AI reply
try:
    reply = generate_reply(message)

except Exception as e:
    print("AI Reply Error:", e)
    reply = "Sorry, we are unable to generate a reply at the moment."


    # Check if customer already exists
    if customer_exists(connection, email):

        update_customer(
            connection,
            email,
            message,
            reply,
            intent,
            department,
            priority,
            sentiment
        )

        print(f"{name} updated successfully.")

    else:

        insert_customer(
            connection,
            name,
            email,
            message,
            reply,
            intent,
            department,
            priority,
            sentiment
        )

        print(f"{name} inserted successfully.")


    # Send email to customer
    send_email(
        email,
        "AI Customer Support Reply",
        reply
    )


    # Display information
    print("Customer:", name)
    print("Email:", email)
    print("Message:", message)
    print("AI Reply:", reply)
    print("Intent:", intent)
    print("Department:", department)
    print("Priority:", priority)
    print("Sentiment:", sentiment)
    print("-" * 50)


# Close database connection
connection.close()

print("Program Finished Successfully!")