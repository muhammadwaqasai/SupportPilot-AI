import os


def load_documents(company_id="company_1"):

    documents = []


    folder = os.path.join(
        "companies",
        company_id,
        "knowledge"
    )


    if not os.path.exists(folder):
        return documents



    for file in os.listdir(folder):

        path = os.path.join(
            folder,
            file
        )


        if file.endswith(".txt"):

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                documents.append({

                    "filename": file,

                    "content": f.read(),

                    "company": company_id

                })


    return documents