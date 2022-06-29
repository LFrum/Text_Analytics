from . import main
def promise():
    text = main.download()
    promises = main.extract_requests(text)
    titles = main.extract_titles(promises)
    randomtitle = main.random_title(titles)
    print(f"A promise: {randomtitle}")
