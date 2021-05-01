import wikipedia


def wikipediaSearch(search_text: str):
    wikipedia.set_lang('ja')
    try:
        url = wikipedia.page(title=search_text, auto_suggest=False, redirect=False).url
        return url
    except:
        return False
