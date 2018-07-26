import wikipedia


def wikiapp(word):
    page = wikipedia.wikipedia.WikipediaPage
    wikipedia.set_lang("ru")
    try:
        page = wikipedia.page(word)
    except wikipedia.exceptions.PageError as pageError:
        print("don' found page")
    except wikipedia.exceptions.DisambiguationError as e:
        page = wikipedia.page(str(e.options[1]))
        print(type(page))
        print("Найденные страницы:\n" + str(e.options))
    finally:
        desc = page.summary
    print(type(page))
    print("_____________________________________________________________")
    return desc


print(wikiapp("sdklhvkldshvlodskvhds"))
