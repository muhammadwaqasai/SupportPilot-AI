from fastembed import TextEmbedding

model = None


def get_model():
    global model

    if model is None:
        model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    return model


def create_embedding(text):
    """
    Convert text into a vector embedding.
    """

    embedding_model = get_model()

    # fastembed returns a generator of numpy arrays
    embedding = list(embedding_model.embed([text]))[0]

    return embedding.tolist()