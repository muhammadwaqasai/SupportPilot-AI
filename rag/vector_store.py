import chromadb
from rag.embeddings import create_embedding


client = None


def get_chroma_client():

    global client

    if client is None:
        client = chromadb.PersistentClient(
            path="chroma_db"
        )

    return client



def get_collection(company_id):

    chroma_client = get_chroma_client()

    return chroma_client.get_or_create_collection(
        name=f"{company_id}_knowledge"
    )




def add_document(text, document_id, company_id):

    """
    Store company-specific document
    """

    collection = get_collection(company_id)


    embedding = create_embedding(text)


    collection.add(

        ids=[document_id],

        documents=[text],

        embeddings=[embedding]

    )


    print(
        f"Document added successfully for {company_id}!"
    )





def search_document(query, company_id, results=3):

    """
    Search only selected company's knowledge
    """


    collection = get_collection(company_id)


    query_embedding = create_embedding(query)



    result = collection.query(

        query_embeddings=[query_embedding],

        n_results=results

    )


    return result
