from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    check_password_hash
)

from mysql_operations import connect_database


# ---------------- FLASK LOGIN SETUP ----------------

login_manager = LoginManager()

login_manager.login_view = "auth.login"

login_manager.login_message = "Please login to access this page."



# ---------------- USER MODEL ----------------

class AdminUser(UserMixin):

    def __init__(
        self,
        id,
        email,
        role,
        company_id
    ):

        self.id = id
        self.email = email
        self.role = role
        self.company_id = company_id



# ---------------- LOAD USER ----------------

@login_manager.user_loader
def load_user(user_id):

    connection = connect_database()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT *
        FROM admin_users
        WHERE id=%s
        """,
        (user_id,)
    )


    user = cursor.fetchone()


    cursor.close()
    connection.close()


    if user:

        return AdminUser(
            user["id"],
            user["email"],
            user["role"],
            user["company_id"]
        )


    return None




# ---------------- AUTH BLUEPRINT ----------------

auth = Blueprint(
    "auth",
    __name__
)




# ---------------- LOGIN ----------------

@auth.route(
    "/login",
    methods=["GET", "POST"]
)
def login():


    if request.method == "POST":


        email = request.form["email"]

        password = request.form["password"]



        connection = connect_database()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT *
            FROM admin_users
            WHERE email=%s
            """,
            (email,)
        )


        user = cursor.fetchone()


        cursor.close()
        connection.close()



        if user and check_password_hash(
            user["password_hash"],
            password
        ):


            admin = AdminUser(
                user["id"],
                user["email"],
                user["role"],
                user["company_id"]
            )


            login_user(admin)


            return redirect(
                url_for("admin")
            )


        flash(
            "Invalid email or password"
        )


    return render_template(
        "login.html"
    )




# ---------------- LOGOUT ----------------

@auth.route("/logout")
@login_required
def logout():


    logout_user()


    return redirect(
        url_for("auth.login")
    )