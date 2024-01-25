from bs4 import BeautifulSoup
import json
import re
import os


def clean_translation(text):
    target = text.replace("\n     ", "").strip()
    target = target.replace("\n", " ")
    target = target.replace("\u200E", "")
    target = target.replace('"', "")
    target = re.sub(r"\[.*?\]", "", target)

    return target


def clean_subtitle(text):
    target = text.replace("\n", " ")
    target = target.replace("\u200E", "")
    target = target.replace('"', "")
    target = re.sub(r"\[.*?\]", "", target)
    target = re.sub(r"-(?![\s-])", "- ", target)
    target = target.strip()

    return target


def process_subtitle(td):
    processed_subtitle = ""
    for element in td.children:
        if element.name == "span":
            text = element.get_text()
            processed_subtitle += text + ""

    processed_subtitle = clean_subtitle(processed_subtitle)
    return processed_subtitle


def process_and_save_data(movies_id, lang_code):
    file_path = f"./markup/en-{lang_code}/{movies_id}.html"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")
        rows = soup.find_all("tr")[1:]

        translations = []
        for row in rows:
            cols = row.find_all("td")
            subtitle = process_subtitle(cols[1])

            if len(cols) >= 3:
                translation = clean_translation(cols[2].get_text())
            else:
                translation = ""

            if subtitle and translation and subtitle != translation:
                translations.append(
                    {
                        "translation": {
                            "en": subtitle,
                            f"{lang_code}": translation,
                        }
                    }
                )

        if not translations:
            raise ValueError(f"No valid translations found for {movies_id}")

        dir_path = f"./data/en-{lang_code}"
        os.makedirs(dir_path, exist_ok=True)

        with open(
            f"./data/en-{lang_code}/{movies_id}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(translations, f, indent=2, ensure_ascii=False)
            print(
                f"The subtitle has been saved as ./data/en-{lang_code}/{movies_id}.json"
            )

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        with open(f"./markup/note-en-{lang_code}.txt", "a", encoding="utf-8") as f:
            f.write(f"Failed to extract {file_path}\n")
    except ValueError as e:
        print(e)
        with open(f"./markup/note-en-{lang_code}.txt", "a", encoding="utf-8") as f:
            f.write(f"Failed to extract {file_path}\n")


netflix_links = []
movies_ids = []

with open("./source/movies_links_cleaned.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith("https://www.netflix.com/watch/"):
            netflix_links.append(line)
            movie_id = line.split("/")[-1]
            movies_ids.append(movie_id)


for i, link in enumerate(netflix_links):
    if 0 <= i <= 1100:
        process_and_save_data(movies_ids[i], "ja")