from rag.retriever import search_knowledge


result = search_knowledge(
    "What is the refund policy?"
)


print(result)