from rag.vector_store import add_document, search_document


text = """
Our company provides online customer support services.

Refund policy:
Customers can request refunds within 30 days of purchase.

Shipping:
Orders are delivered within 5 business days.

Customer support email:
support@company.com
"""


# Add knowledge
add_document(
    text,
    "company_info_1"
)


# Search
answer = search_document(
    "How many days does delivery take?"
)


print(answer)