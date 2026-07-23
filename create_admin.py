from mysql_operations import connect_database

from werkzeug.security import generate_password_hash



def create_admin():

    email = input(
        "Admin email: "
    )

    password = input(
        "Password: "
    )

    role = input(
        "Role (company_admin/super_admin): "
    )


    company_id = None


    if role == "company_admin":

        company_id = input(
            "Company ID: "
        )



    password_hash = generate_password_hash(
        password
    )


    connection = connect_database()

    cursor = connection.cursor()


    query = """
    INSERT INTO admin_users
    (
        email,
        password_hash,
        role,
        company_id
    )

    VALUES
    (%s,%s,%s,%s)
    """



    cursor.execute(

        query,

        (
            email,
            password_hash,
            role,
            company_id
        )

    )


    connection.commit()


    cursor.close()

    connection.close()


    print(
        "Admin created successfully!"
    )



if __name__ == "__main__":

    create_admin()