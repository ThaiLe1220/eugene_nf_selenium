import re
import os
import json


def delete_invalid_translation_files(directory, lang_code):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as datafile:
                    data = json.load(datafile)

                repetitive_count = 0
                for item in data:
                    en = item["translation"]["en"]
                    lang_translation = item["translation"].get(lang_code)
                    if en == lang_translation or en == "" or lang_translation == "":
                        repetitive_count += 1
                        if repetitive_count >= 65:
                            os.remove(file_path)
                            print(
                                f"Deleted file due to repetitive translations: {filename}"
                            )
                            break

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {filename}")
            except PermissionError:
                print(
                    f"Cannot delete file, it's being used by another process: {filename}"
                )


def clean_text(text):
    text = text.replace("♪ ", "")
    text = text.replace(" ♪", "")
    text = text.replace("- -", " ")
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"^[A-Z]+: ", "", text)

    return text.strip()


def clean_translations_data(directory, lang_code, movie_ids):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                item["translation"]["en"] = clean_text(item["translation"]["en"])
                item["translation"][f"{lang_code}"] = clean_text(
                    item["translation"][f"{lang_code}"]
                )

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)


LANG_CODE = "es"
DIRECTORY = f"../data/en-{LANG_CODE}"

NETFLIX_LINKS = []
MOVIE_IDS = []

# Read the links from the movies_links.txt file and add them to the list
with open("../source/movies_links_cleaned.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line.startswith("https://www.netflix.com/watch/"):
            NETFLIX_LINKS.append(line)
            movie_id = line.split("/")[-1]
            MOVIE_IDS.append(movie_id)


delete_invalid_translation_files(DIRECTORY, LANG_CODE)
clean_translations_data(DIRECTORY, LANG_CODE, MOVIE_IDS)
