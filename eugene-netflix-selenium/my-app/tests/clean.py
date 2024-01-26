import re


def clean_text(text):
    # text = text.replace("♪", "")
    text = text.replace("\n", "")
    text = text.replace("\u200E", "")

    # Uncomment these lines if you want to remove any text inside parentheses and any word that is in uppercase followed by a colon.
    # text = re.sub(r"\(.*?\)", "", text)
    # text = re.sub(r"^[A-Z]+: ", "", text)

    return text.strip()


# List of provided translation data
translations = [
    {
        "en": "That this place is damned. [SCOFFS]\n\n\n",
        "fr": "\n                        \n                        Que ce lieu est damné.\n                        \n                    ",
    },
    {
        "en": "Well, she-she was European.\n\n\n",
        "fr": "\n                        \n                        - Elle était européenne.\n- D'accord.\n                        \n                    ",
    },
    {
        "en": "Wanna write that down for me, Frank? So I can say it to Zee?\n\n\n",
        "fr": "\n                        \n                        Ecris-le-moi.\nJe veux le dire à Zee.\n                        \n                    ",
    },
    {
        "en": "You ever-- Ever notice Zerelda's eyes?\n\n\n",
        "fr": "\n                        \n                        Tu as vu les yeux de Zerelda ?\n                        \n                    ",
    },
    {"en": "- An extra $100. - Twenty!", "fr": "- 100 $ de plus. - 20 $."},
]

# Test each case
for idx, data in enumerate(translations):
    cleaned_en = clean_text(data["en"])
    cleaned_fr = clean_text(data["fr"])

    # Print the cleaned results
    print(f"Case {idx + 1}: '{cleaned_en}'")
    print(f"Case {idx + 1}: '{cleaned_fr}'")
    print()
