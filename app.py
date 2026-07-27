from flask import Flask, render_template, request, redirect
from flask_login import (
    login_required,
    current_user
)
from services.report_service import generate_business_report
from services.root_cause_service import analyze_root_causes
from services.trend_service import analyze_trends
from mysql_operations import get_recent_customer_insights
from services.business_ai_service import generate_ai_business_report
from services.business_advisor_service import generate_business_advice

from auth import (
    auth,
    login_manager
)

from config import (
    SECRET_KEY,
    PERMANENT_SESSION_LIFETIME
)

from mysql_operations import (
    connect_database,
    get_business_statistics,
    get_all_customers,
    search_customers,
    delete_customer,
    edit_customer,
    approve_ticket,
    save_learning_example,
    get_ticket_trends
)

from services.customer_service import process_customer
from email_sender import send_email
from services.analytics_service import generate_dashboard_analytics
from services.company_service import get_companies
from logger import log_info
from services.learning_analytics_service import generate_learning_analytics


app = Flask(__name__)
import traceback

@app.errorhandler(Exception)
def handle_error(e):
    print("ERROR:", e)
    traceback.print_exc()
    return "Internal Server Error", 500
app.secret_key = SECRET_KEY


app.config[
    "PERMANENT_SESSION_LIFETIME"
] = PERMANENT_SESSION_LIFETIME


login_manager.init_app(app)


app.register_blueprint(auth)



# ---------------- HOME CUSTOMER FORM ----------------

@app.route("/")
def landing():

    return render_template(
        "landing.html"
    )
@app.route("/favicon.ico")
def favicon():
    return "", 204
@app.route("/demo", methods=["GET", "POST"])
def home():

    companies = get_companies()



    if request.method == "POST":


        name = request.form["customer_name"]

        email = request.form["email"]

        message = request.form["message"]


        company_id = request.form.get(
            "company_id",
            "company_1"
        )



        connection = connect_database()



        try:

            process_customer(

                connection,

                name,

                email,

                message,

                company_id

            )


            cursor = connection.cursor(dictionary=True)


            cursor.execute(
                """
                SELECT *
                FROM customers
                WHERE email=%s
                AND company_id=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (
                    email,
                    company_id
                )
            )


            customer = cursor.fetchone()
            print(customer)


            cursor.close()



        finally:

            connection.close()



        return render_template(
            "demo_result.html",
            customer=customer
        )



    return render_template(
        "index.html",
        companies=companies
    )





# ---------------- ADMIN DASHBOARD ----------------


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():

    connection = connect_database()

    try:

        if request.method == "POST":

            keyword = request.form["keyword"]

            if current_user.role == "super_admin":

                customers = search_customers(
                    connection,
                    keyword
                )

            else:

                customers = search_customers(
                    connection,
                    keyword,
                    current_user.company_id
                )


        else:

            if current_user.role == "super_admin":

                customers = get_all_customers(
                    connection
                )

            else:

                customers = get_all_customers(
                    connection,
                    current_user.company_id
                )


        print(
            "LOGIN COMPANY:",
            current_user.company_id
        )


        for customer in customers:

            print(
                "DASHBOARD:",
                customer["id"],
                customer["company_id"]
            )


        analytics = generate_dashboard_analytics(
            customers
        )


    finally:

        connection.close()
        waiting_review_count = 0

        for customer in customers:

            if customer["status"] == "Waiting Review":

                waiting_review_count += 1


    return render_template(

    "admin.html",

    customers=customers,

    total_customers=analytics["total_customers"],

    high_priority=analytics["high_priority"],

    negative_sentiment=analytics["negative_sentiment"],

    completed_cases=analytics["completed_cases"],

    ai_solved_cases=analytics["ai_solved_cases"],

    ai_solved_percentage=analytics["ai_solved_percentage"],

    human_review_cases=analytics["human_review_cases"],

    human_review_percentage=analytics["human_review_percentage"],

    escalation_cases=analytics["escalation_cases"],

    escalation_percentage=analytics["escalation_percentage"],

    high_risk_cases=analytics["high_risk_cases"],

    average_confidence=analytics["average_confidence"],

    priority_data=analytics["priority_data"],

    sentiment_data=analytics["sentiment_data"],

    department_data=analytics["department_data"]

)

# ---------------- AI TICKET DETAIL ----------------

@app.route("/ticket/<int:id>")
@login_required
def ticket_detail(id):

    connection = connect_database()

    cursor = connection.cursor(dictionary=True)


    cursor.execute(
        "SELECT * FROM customers WHERE id=%s",
        (id,)
    )

    customer = cursor.fetchone()


    cursor.close()
    connection.close()


    if customer is None:
        return "Ticket not found", 404



    # Permission check

    if current_user.role != "super_admin":

        if customer["company_id"] != current_user.company_id:

            return "Access Denied", 403



    return render_template(
        "ticket_detail.html",
        customer=customer
    )






# ---------------- DELETE ----------------

@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    connection = connect_database()

    try:

        cursor = connection.cursor(dictionary=True)


        # Check ticket ownership

        if current_user.role == "super_admin":

            cursor.execute(
                """
                SELECT id
                FROM customers
                WHERE id=%s
                """,
                (id,)
            )

        else:

            cursor.execute(
                """
                SELECT id
                FROM customers
                WHERE id=%s
                AND company_id=%s
                """,
                (
                    id,
                    current_user.company_id
                )
            )


        ticket = cursor.fetchone()

        cursor.close()


        if ticket is None:

            return """
            <h2>Access Denied</h2>
            <a href="/admin">Back</a>
            """


        delete_customer(
            connection,
            id
        )


        return """
        <h2>Customer deleted successfully!</h2>
        <a href="/admin">Back</a>
        """


    finally:

        connection.close()







# ---------------- EDIT ----------------

@app.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit(id):

    connection = connect_database()

    try:

        cursor = connection.cursor(dictionary=True)


        # Get ticket with company security check

        if current_user.role == "super_admin":

            cursor.execute(
                """
                SELECT *
                FROM customers
                WHERE id=%s
                """,
                (id,)
            )

        else:

            cursor.execute(
                """
                SELECT *
                FROM customers
                WHERE id=%s
                AND company_id=%s
                """,
                (
                    id,
                    current_user.company_id
                )
            )


        customer = cursor.fetchone()


        cursor.close()


        # Ticket does not belong to this admin

        if customer is None:

            return """
            <h2>Access Denied</h2>
            <a href="/admin">Back</a>
            """



        if request.method == "POST":


            edit_customer(

                connection,

                id,

                request.form["customer_name"],

                request.form["email"],

                request.form["message"],

                request.form["status"],

                request.form["assigned_agent"],

                request.form["agent_note"],

                current_user.company_id

            )


            return """
            <h2>Ticket updated successfully!</h2>
            <a href="/admin">Back</a>
            """



        return render_template(
            "edit_customer.html",
            customer=customer
        )


    finally:

        connection.close()
        # ---------------- APPROVE WAITING REVIEW TICKET ----------------


@app.route("/approve/<int:id>", methods=["POST"])
@login_required
def approve(id):

    connection = connect_database()

    try:

        cursor = connection.cursor(dictionary=True)


        # Get ticket

        cursor.execute(
            """
            SELECT *
            FROM customers
            WHERE id=%s
            """,
            (id,)
        )

        customer = cursor.fetchone()


        cursor.close()


        if customer is None:

            return "Ticket not found", 404



        # Company security check

        if current_user.role != "super_admin":

            if customer["company_id"] != current_user.company_id:

                return "Access Denied", 403



        # Approve ticket

        approve_ticket(
            connection,
            id,
            current_user.email
        )


        # Send approved reply

        send_email(

            customer["email"],

            "AI Customer Support Reply",

            customer["ai_reply"]

        )


        log_info(
            f"Ticket approved by {current_user.email}: {id}"
        )


        return """
        <h2>
        Ticket approved and email sent successfully!
        </h2>

        <a href="/admin">
        Back to Dashboard
        </a>
        """


    finally:

        connection.close()

@app.route("/edit_reply/<int:id>", methods=["GET", "POST"])
@login_required
def edit_reply(id):

    connection = connect_database()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM customers
        WHERE id=%s
        """,
        (id,)
    )

    customer = cursor.fetchone()

    if customer is None:

        cursor.close()
        connection.close()

        return "Customer not found"

    if request.method == "POST":

        edited_reply = request.form["reply"]
        cursor.execute(
            """
            UPDATE customers
            SET
                ai_reply=%s,
                status='Completed',
                approved_by=%s,
                approved_at=NOW(),
                was_edited=TRUE
            WHERE id=%s
            """,
            (
                edited_reply,
                current_user.email,
                id
            )
        )

        connection.commit()

        send_email(
            customer["email"],
            "AI Customer Support Reply",
            edited_reply
        )

        save_learning_example(
            connection,
            customer["message"],
            customer["ai_reply"],
            edited_reply,
            customer["intent"],
            customer["company_id"],
            current_user.email
        )

        log_info(
            f"Ticket approved by {current_user.email}: {id}"
        )

        cursor.close()
        connection.close()

        return redirect("/admin")

    cursor.close()
    connection.close()

    return render_template(
        "edit_reply.html",
        customer=customer
    )
    
     # ---------------- AI LEARNING REVIEW ----------------

@app.route("/ai-learning")
@login_required
def ai_learning():

    connection = connect_database()

    try:

        cursor = connection.cursor(dictionary=True)


        if current_user.role == "super_admin":

            cursor.execute(
                """
                SELECT *
                FROM ai_learning
                ORDER BY id DESC
                """
            )

        else:

            cursor.execute(
                """
                SELECT *
                FROM ai_learning
                WHERE company_id=%s
                ORDER BY id DESC
                """,
                (current_user.company_id,)
            )


        learning_examples = cursor.fetchall()
        cursor.execute(
    """
    SELECT *
    FROM ai_learning_versions
    ORDER BY id DESC
    """
)

        learning_versions = cursor.fetchall()
        learning_analytics = generate_learning_analytics(
    learning_examples
)

        cursor.close()


    finally:

        connection.close()


    return render_template(
    "ai_learning.html",
    learning_examples=learning_examples,
    learning_analytics=learning_analytics,
    learning_versions=learning_versions
)
    
    # ---------------- APPROVE AI LEARNING ----------------

@app.route("/approve-learning/<int:id>", methods=["POST"])
@login_required
def approve_learning(id):

    connection = connect_database()

    try:

        cursor = connection.cursor()


        cursor.execute(
            """
            UPDATE ai_learning
            SET
                review_status='Approved',
                reviewed_by=%s,
                reviewed_at=NOW()
            WHERE id=%s
            """,
            (
                current_user.email,
                id
            )
        )


        connection.commit()

        cursor.close()


    finally:

        connection.close()


    return redirect("/ai-learning")

# ---------------- REJECT AI LEARNING ----------------

@app.route("/reject-learning/<int:id>", methods=["POST"])
@login_required
def reject_learning(id):

    connection = connect_database()

    try:

        cursor = connection.cursor()


        cursor.execute(
            """
            UPDATE ai_learning
            SET
                review_status='Rejected',
                reviewed_by=%s,
                reviewed_at=NOW()
            WHERE id=%s
            """,
            (
                current_user.email,
                id
            )
        )


        connection.commit()

        cursor.close()


    finally:

        connection.close()


    return redirect("/ai-learning")

@app.route("/business_advisor")
@login_required
def business_advisor():

    connection = connect_database()

    stats = get_business_statistics(
        connection,
        current_user.company_id
    )


    tickets = get_recent_customer_insights(
        connection,
        current_user.company_id
    )


    trend_data = get_ticket_trends(
        connection,
        current_user.company_id
    )


    connection.close()


    # Old rule-based advice
    advice = generate_business_advice(stats)


    # AI Executive Report
    ai_report = generate_ai_business_report(
        stats
    )


    # AI Root Cause Analysis
    root_cause = analyze_root_causes(
        tickets
    )


    # AI Trend Analysis
    trend_report = analyze_trends(
        trend_data
    )


    return render_template(
        "business_advisor.html",
        stats=stats,
        advice=advice,
        ai_report=ai_report,
        root_cause=root_cause,
        trend_report=trend_report
    )
    # ---------------- BUSINESS REPORT PDF ----------------

@app.route("/generate_report")
@login_required
def generate_report():

    connection = connect_database()

    stats = get_business_statistics(
        connection,
        current_user.company_id
    )

    tickets = get_recent_customer_insights(
        connection,
        current_user.company_id
    )

    trend_data = get_ticket_trends(
        connection,
        current_user.company_id
    )

    connection.close()

    ai_report = generate_ai_business_report(
        stats
    )

    root_cause = analyze_root_causes(
        tickets
    )

    trend_report = analyze_trends(
        trend_data
    )

    # Save directly into the static folder
    filename = "static/business_report.pdf"

    generate_business_report(
        filename,
        stats,
        ai_report,
        root_cause,
        trend_report
    )

    return redirect("/static/business_report.pdf")


# ---------------- RUN APP ----------------

if __name__ == "__main__":


    app.run(debug=True)
   
   
