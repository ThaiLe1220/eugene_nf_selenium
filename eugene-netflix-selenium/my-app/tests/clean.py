import re


def clean_text(text):
    text = text.replace("♪ ", "")
    text = text.replace(" ♪", "")
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"^[A-Z]+: ", "", text)
    text = text.replace("- -", " ")

    return text.strip()
