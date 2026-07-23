from rag.vector_store import search_document
from ai_reply import generate_reply


def rag_answer(customer_question):
    """
    RAG based AI response
    """

    # Search company knowledge
    knowledge = search_document(
        customer_question,
        results=1
    )

    documents = knowledge["documents"]

    if documents and documents[0]:
        context = documents[0][0]
    else:
        context = "No company information available."


    # Generate AI reply using context
    prompt = f"""
You are an AI customer support agent.

Use this company information:

{context}

Customer question:
{customer_question}

Give a helpful professional reply.
"""

    answer = generate_reply(prompt)

    return answer