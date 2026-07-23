import os

from rag.vector_store import add_document



def create_company_vectors():


    companies_folder = "companies"



    if not os.path.exists(companies_folder):

        print("Companies folder not found!")

        return




    for company_id in os.listdir(companies_folder):


        company_path = os.path.join(
            companies_folder,
            company_id
        )



        knowledge_path = os.path.join(
            company_path,
            "knowledge"
        )



        if not os.path.isdir(knowledge_path):

            continue




        print(
            f"\nLoading knowledge for {company_id}"
        )



        for file in os.listdir(knowledge_path):


            if file.endswith(".txt"):


                file_path = os.path.join(
                    knowledge_path,
                    file
                )



                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()



                document_id = (
                    company_id
                    + "_"
                    + file
                )



                add_document(

                    content,

                    document_id,

                    company_id

                )




    print("\nAll company vectors created successfully!")




if __name__ == "__main__":

    create_company_vectors()