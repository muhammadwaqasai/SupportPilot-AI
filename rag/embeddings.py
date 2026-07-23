from sentence_transformers import SentenceTransformer

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text):
    """
    Convert text into a vector embedding.
    """
    return model.encode(text).tolist()