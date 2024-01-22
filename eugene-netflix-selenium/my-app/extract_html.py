from bs4 import BeautifulSoup
import json
import re


def clean_text(text):
    return text.replace("\n                    ", " ").strip()


def process_subtitle(td):
    processed_subtitle = ""
    for element in td.children:
        if element.name == "span":
            text = element.get_text()
            text = text.replace("\n", " ")
            processed_subtitle += text + ""

    return processed_subtitle.strip()


def process_and_save_data(movies_id):
    file_path = f"./markup/{movies_id}.html"

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
        translation = clean_text(cols[2].get_text())

        # Check for machine translation
        if len(cols) == 4:
            machine_translation = clean_text(cols[3].get_text())
        else:
            machine_translation = ""  # No machine translation available

            translations.append(
                {
                    "subtitle": {
                        "time": time,
                        "subtitle": subtitle,
                        "translation": translation,
                        "machine_translation": machine_translation,
                    }
                }
            )

    with open(f"./data/{movies_id}.json", "w", encoding="utf-8") as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)
        print(f"The subtitle has been saved as ./data/{movies_id}.json")
