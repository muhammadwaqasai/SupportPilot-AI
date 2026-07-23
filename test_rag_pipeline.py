from rag.rag_pipeline import rag_answer


question = "How long does shipping take?"


response = rag_answer(question)


print("\nAI Response:")
print(response)