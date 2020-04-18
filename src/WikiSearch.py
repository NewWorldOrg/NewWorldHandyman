import wikipedia

def wikipediaSearch(search_text: str):
    wikipedia.set_lang('ja')
    try:
        url = wikipedia.page(search_text).url
        return  url
    except:
        return False
