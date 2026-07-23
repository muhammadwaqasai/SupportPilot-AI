import mysql.connector

from config import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


# ---------------- DATABASE CONNECTION ----------------

def connect_database():

    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    return connection



# ---------------- CHECK CUSTOMER ----------------

def customer_exists(connection, email, company_id):

    cursor = connection.cursor()

    query = """
    SELECT COUNT(*)
    FROM customers
    WHERE email = %s
    AND company_id = %s
    """

    cursor.execute(query, (email, company_id))

    result = cursor.fetchone()[0]

    cursor.close()

    return result > 0



# ---------------- INSERT CUSTOMER ----------------

def insert_customer(
        connection,
        name,
        email,
        message,
        ai_reply,
        intent,
        department,
        priority,
        sentiment,
        summary,
        recommended_action,
        risk_level,
        escalation,
        confidence_score,
        company_id
):

    cursor = connection.cursor()

    query = """
    INSERT INTO customers
    (
        customer_name,
        email,
        message,
        ai_reply,
        status,
        intent,
        department,
        priority,
        sentiment,
        summary,
        recommended_action,
        risk_level,
        escalation,
        confidence_score,
        company_id
    )

    VALUES
    (
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s
    )
    """

    values = (

        name,
        email,
        message,
        ai_reply,
        "Completed",

        intent,
        department,
        priority,
        sentiment,

        summary,
        recommended_action,
        risk_level,
        escalation,
        confidence_score,

        company_id

    )


    cursor.execute(query, values)

    connection.commit()

    cursor.close()



# ---------------- UPDATE CUSTOMER ----------------

def update_customer(
        connection,
        email,
        message,
        ai_reply,
        intent,
        department,
        priority,
        sentiment,
        summary,
        recommended_action,
        risk_level,
        escalation,
        confidence_score
):

    cursor = connection.cursor()

    query = """

    UPDATE customers

    SET

        message=%s,
        ai_reply=%s,
        status=%s,

        intent=%s,
        department=%s,
        priority=%s,
        sentiment=%s,

        summary=%s,
        recommended_action=%s,
        risk_level=%s,
        escalation=%s,
        confidence_score=%s


    WHERE email=%s

    """

    values = (

        message,
        ai_reply,
        "Completed",

        intent,
        department,
        priority,
        sentiment,

        summary,
        recommended_action,
        risk_level,
        escalation,
        confidence_score,

        email

    )


    cursor.execute(query, values)

    connection.commit()

    cursor.close()



# ---------------- GET ALL CUSTOMERS ----------------

def get_all_customers(connection, company_id=None):

    cursor = connection.cursor(dictionary=True)

    if company_id is None:

        query = """
        SELECT *
        FROM customers
        """

        cursor.execute(query)

    else:

        query = """
        SELECT *
        FROM customers
        WHERE company_id=%s
        """

        cursor.execute(
            query,
            (company_id,)
        )

    customers = cursor.fetchall()

    cursor.close()

    return customers

# ---------------- SEARCH CUSTOMERS ----------------

def search_customers(connection, keyword, company_id=None):

    cursor = connection.cursor(dictionary=True)

    value = "%" + keyword + "%"


    if company_id is None:

        query = """
        SELECT *
        FROM customers
        WHERE customer_name LIKE %s
        OR email LIKE %s
        """

        cursor.execute(
            query,
            (value, value)
        )

    else:

        query = """
        SELECT *
        FROM customers
        WHERE company_id=%s
        AND
        (
            customer_name LIKE %s
            OR email LIKE %s
        )
        """

        cursor.execute(
            query,
            (
                company_id,
                value,
                value
            )
        )


    customers = cursor.fetchall()

    cursor.close()

    return customers

# ---------------- DELETE CUSTOMER ----------------

def delete_customer(connection, customer_id, company_id):

    cursor = connection.cursor()

    cursor.execute(
    """
    DELETE FROM customers
    WHERE id=%s
    AND company_id=%s
    """,
    (
        customer_id,
        company_id
    )
)

    connection.commit()

    cursor.close()



# ---------------- EDIT CUSTOMER ----------------

def edit_customer(
        connection,
        customer_id,
        name,
        email,
        message,
        status,
        assigned_agent=None,
        agent_note=None,
        company_id=None
):

    cursor = connection.cursor()

    query = """

    UPDATE customers

    SET

        customer_name=%s,
        email=%s,
        message=%s,
        status=%s,
        assigned_agent=%s,
        agent_note=%s


    WHERE id=%s
AND company_id=%s

    """

    values = (

    name,
    email,
    message,
    status,
    assigned_agent,
    agent_note,
    customer_id,
    company_id

)


    cursor.execute(query, values)

    connection.commit()

    cursor.close()



# ---------------- CUSTOMER MEMORY ----------------

def get_customer_history(connection, email, company_id):

    cursor = connection.cursor(dictionary=True)

    query = """

    SELECT

        message,
        ai_reply,
        intent,
        department,
        priority,
        status


    FROM customers


    WHERE email=%s
    AND company_id=%s


    ORDER BY id DESC


    LIMIT 5

    """


    cursor.execute(
        query,
        (email, company_id)
    )


    history = cursor.fetchall()


    cursor.close()


    return history
def update_ticket_status(
    connection,
    email,
    status
):

    cursor = connection.cursor()

    query = """
    UPDATE customers
    SET status=%s
    WHERE email=%s
    """

    cursor.execute(
        query,
        (
            status,
            email
        )
    )

    connection.commit()

    cursor.close()
    # ---------------- APPROVE TICKET ----------------

def approve_ticket(
        connection,
        ticket_id,
        admin_email,
        edited_reply=None
):

    cursor = connection.cursor()


    if edited_reply:

     query = """
    UPDATE customers

    SET
        ai_reply=%s,
        status='Completed',
        approved_by=%s,
        approved_at=NOW(),
        was_edited=TRUE

    WHERE id=%s
    """


     values = (
            edited_reply,
            admin_email,
            ticket_id
        )


    else:

     query = """
    UPDATE customers

    SET
        status='Completed',
        approved_by=%s,
        approved_at=NOW(),
        was_edited=FALSE

    WHERE id=%s
    """


     values = (
            admin_email,
            ticket_id
        )


    cursor.execute(
        query,
        values
    )

    connection.commit()

    cursor.close()


def save_learning_example(
    connection,
    customer_message,
    original_ai_reply,
    approved_reply,
    intent,
    company_id,
    approved_by
):

    cursor = connection.cursor()

    query = """
    INSERT INTO ai_learning
    (
        customer_message,
        original_ai_reply,
        approved_reply,
        intent,
        company_id,
        approved_by
    )
    VALUES
    (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            customer_message,
            original_ai_reply,
            approved_reply,
            intent,
            company_id,
            approved_by
        )
    )

    connection.commit()

    cursor.close()   