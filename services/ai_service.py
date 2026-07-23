from ai_engine import analyze_customer_message

from rag.retriever import search_knowledge



def get_ai_customer_analysis(
        message,
        history=None,
        company_id="company_1"
):


    # Get company knowledge from RAG

    rag_reply = search_knowledge(
        message,
        company_id
    )



    # AI analysis

    analysis = analyze_customer_message(
        message,
        history
    )



    # Add RAG answer

    analysis["rag_reply"] = rag_reply



    return analysis