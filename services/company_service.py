import os



COMPANIES_FOLDER = "companies"



def get_companies():

    companies = []


    if not os.path.exists(COMPANIES_FOLDER):

        return companies



    for company in os.listdir(COMPANIES_FOLDER):


        company_path = os.path.join(
            COMPANIES_FOLDER,
            company
        )


        if os.path.isdir(company_path):

            companies.append(company)



    return companies





def create_company(company_name):


    # Create company folder

    company_folder = os.path.join(
        COMPANIES_FOLDER,
        company_name
    )



    knowledge_folder = os.path.join(
        company_folder,
        "knowledge"
    )



    if os.path.exists(company_folder):

        return False



    os.makedirs(
        knowledge_folder
    )



    # Create empty knowledge file

    file_path = os.path.join(
        knowledge_folder,
        "company_info.txt"
    )


    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{company_name} knowledge base\n"
        )



    return True





def company_exists(company_name):


    path = os.path.join(
        COMPANIES_FOLDER,
        company_name
    )


    return os.path.exists(path)