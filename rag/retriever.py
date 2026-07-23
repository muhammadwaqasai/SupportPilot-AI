from rag.vector_store import search_document



def search_knowledge(query, company_id):


    result = search_document(

        query,

        company_id,

        results=1

    )


    if not result["documents"]:

        return "No company information available."



    documents = result["documents"][0]



    if documents:

        return documents[0]



    return "No matching information found."