
def qa_automation_python():
    search = "https://hh.ru/search/vacancy?"
    text = "text=Qa+automation+Python"
    url = search + text + "&salary=&ored_clusters=true&enable_snippets=true"
    return url, 4, "QA_Automation_Python"


def qa_manual():
    search = "https://hh.ru/search/vacancy?"
    search_f = "search_field=name&search_field=company_name&search_field=description"
    url = search + search_f + "&enable_snippets=true&text=Manual+qa&from=suggest_post"
    return url, 5, "QA_manual"


def qa_middle():
    search = "https://hh.ru/search/vacancy?"
    url = search + "text=qa+middle&salary=&ored_clusters=true&enable_snippets=true"
    return url, 9, "QA_middle"
