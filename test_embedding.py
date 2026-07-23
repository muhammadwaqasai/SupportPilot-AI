from rag.embeddings import create_embedding

vector = create_embedding("Our company provides refund within 30 days.")

print("Vector created successfully!")
print("Vector length:", len(vector))
print("First 10 values:", vector[:10])