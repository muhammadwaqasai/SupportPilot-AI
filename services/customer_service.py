from mysql_operations import (
    customer_exists,
    insert_customer,
    update_customer,
    get_customer_history,
    update_ticket_status,
) 
from services.confidence_service import evaluate_ticket

from services.ai_service import get_ai_customer_analysis
from email_sender import send_email
from logger import log_info, log_error

from rag.retriever import search_knowledge



def process_customer(connection, name, email, message, company_id):

    original_message = message

    log_info(
        f"New customer request received: {email}"
    )

    try:

        # Customer previous history

        history = get_customer_history(
            connection,
            email,
            company_id
        )

        log_info(
            f"Customer history loaded: {email}"
        )


        # ---------------- RAG SEARCH ----------------

        rag_reply = None

        try:

            rag_reply = search_knowledge(
                message,
                company_id
            )

        except Exception as e:

            log_error(
                f"RAG search failed: {e}"
            )


                # Add company knowledge into AI context only

        if rag_reply:

            ai_context = (
                "Company Knowledge:\n"
                + rag_reply
                + "\n\nCustomer Message:\n"
                + original_message
            )

        else:

            ai_context = original_message


        # ---------------- AI ANALYSIS ----------------

        analysis = get_ai_customer_analysis(
            ai_context,
            history,
            company_id
        )


        log_info(
            f"AI analysis completed: {email}"
        )

        # Use AI generated reply
        # RAG is only used as knowledge context

        reply = analysis["reply"]

        

        # Decide what to do with this ticket

        decision = evaluate_ticket(
            analysis["confidence_score"],
            analysis["escalation"],
            analysis["risk_level"]
        )


        # Existing customer update

        if customer_exists(
            connection,
            email,
            company_id
        ):

            update_customer(

                connection,

                email,

                original_message,

                reply,

                analysis["intent"],

                analysis["department"],

                analysis["priority"],

                analysis["sentiment"],

                analysis["summary"],

                analysis["recommended_action"],

                analysis["risk_level"],

                analysis["escalation"],

                analysis["confidence_score"]

            )

            log_info(
                f"Existing customer updated: {email}"
            )

        # New customer insert

        else:

            insert_customer(

                connection,

                name,

                email,

                original_message,

                reply,

                analysis["intent"],

                analysis["department"],

                analysis["priority"],

                analysis["sentiment"],

                analysis["summary"],

                analysis["recommended_action"],

                analysis["risk_level"],

                analysis["escalation"],

                analysis["confidence_score"],

                company_id

            )

            log_info(
                f"New customer inserted: {email}"
            )


        # Update ticket status for BOTH new and existing customers

        update_ticket_status(
            connection,
            email,
            decision["status"]
        )
        log_info(
            f"Ticket status updated to: {decision['status']}"
        )


        # Send email only for approved tickets

        if decision["auto_send"]:

            try:

                send_email(

                    email,

                    "AI Customer Support Reply",

                    reply

                )

                log_info(
                    f"Email sent successfully: {email}"
                )

            except Exception as e:

                log_error(
                    f"Email sending failed for {email}: {e}"
                )


        else:

            log_info(
                f"Email held for manual review: {email}"
            )


        log_info(
            f"Customer process completed successfully: {email}"
        )

        return analysis


    except Exception as e:

        log_error(
            f"Customer processing failed for {email}: {e}"
        )

        raise

       