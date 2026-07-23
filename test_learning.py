from mysql_operations import connect_database
from services.learning_service import get_approved_learning_examples


connection = connect_database()


examples = get_approved_learning_examples(
    connection,
    "company_1"
)


for example in examples:

    print("----------------")
    print("Message:")
    print(example["customer_message"])

    print("Intent:")
    print(example["intent"])

    print("Approved Reply:")
    print(example["approved_reply"])


connection.close()