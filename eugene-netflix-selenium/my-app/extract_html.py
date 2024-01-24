from bs4 import BeautifulSoup
import json
import re


def clean_text(text):
    target = text.replace("\n                    ", " ").strip()
    target = target.replace("\n", " ")
    target = target.replace("\u200E", "")
    target = target.replace('"', "")
    return target


def process_subtitle(td):
    processed_subtitle = ""
    for element in td.children:
        if element.name == "span":
            text = element.get_text()
            text = text.replace("\n", " ")
            processed_subtitle += text + ""

    return processed_subtitle.strip()


def process_and_save_data(movies_id, lang_code):
    file_path = f"./markup/en-{lang_code}/{movies_id}.html"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        rows = soup.find_all("tr")[1:]  # Skip the header row

        # Process each row
        translations = []
        for row in rows:
            cols = row.find_all("td")
            time = cols[0].get_text(strip=True)
            subtitle = process_subtitle(cols[1])

            # Check for machine translation
            if len(cols) >= 3:
                translation = clean_text(cols[2].get_text())
            else:
                translation = ""

            if len(cols) == 4:
                machine_translation = clean_text(cols[3].get_text())
            else:
                machine_translation = ""  # No machine translation available

            # translations.append(
            #     {
            #         "subtitle": {
            #             "time": time,
            #             "subtitle": subtitle,
            #             "translation": translation,
            #             "machine_translation": machine_translation,
            #         }
            #     }
            # )

            translations.append(
                {
                    "translation": {
                        "en": subtitle,
                        f"{lang_code}": translation,
                    }
                }
            )

        with open(
            f"./data/en-{lang_code}/{movies_id}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(translations, f, indent=2, ensure_ascii=False)
            print(
                f"The subtitle has been saved as ./data/en-{lang_code}/{movies_id}.json"
            )

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        with open(f"./markup/note.txt", "a", encoding="utf-8") as file:
            file.write(f"Failed to extract {file_path}")


# netflix_links = []
# movies_ids = []

# # Read the links from the movies_links.txt file and add them to the list
# with open("./source/movies_links_cleaned.txt", "r") as file:
#     for line in file:
#         line = line.strip()
#         if line.startswith("https://www.netflix.com/watch/"):
#             netflix_links.append(line)
#             movie_id = line.split("/")[-1]
#             movies_ids.append(movie_id)


# for i, link in enumerate(netflix_links):
#     if i >= 0:
#         process_and_save_data(movies_ids[i], "es")
