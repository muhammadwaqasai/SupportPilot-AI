def load_knowledge():

    file_path = "knowledge/company_info.txt"

    with open(file_path, "r", encoding="utf-8") as file:

        knowledge = file.read()

    return knowledge