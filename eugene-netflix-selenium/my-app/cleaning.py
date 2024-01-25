import re
import os
import json


def clean_netflix_inacessible_links(input_file, output_file, lang_code):
    cleaned_links = []

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("https://www.netflix.com/watch/"):
                movie_id = re.split(r"[^0-9]", line.split("/")[-1])[0]
                cleaned_link = f"https://www.netflix.com/watch/{movie_id}"
                cleaned_links.append(cleaned_link)

    unique_sorted_links = sorted(
        set(cleaned_links), key=lambda x: int(x.split("/")[-1])
    )

    directory = f"./markup/en-{lang_code}/"
    markup_files = os.listdir(directory)

    # Check if the movie_id is in the markup file names
    inaccessible_links = [
        link
        for link in unique_sorted_links
        if not any(movie_id in file for file in markup_files)
    ]
    file_count = len(
        [
            name
            for name in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, name))
        ]
    )
    print(f"There are {file_count} files in {directory}")

    # Write the accessible links to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        for link in inaccessible_links:
            file.write(link + "\n")


def delete_invalid_translation_files(directory, lang_code):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                repetitive_count = 0
                for item in data:
                    en = item["translation"]["en"]
                    lang_translation = item["translation"].get(lang_code)
                    if en == lang_translation or en == "" or lang_translation == "":
                        repetitive_count += 1
                        if repetitive_count >= 80:
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


def clean_translation(text):
    original_text = text
    text = text.replace("♪ ", "")
    text = text.replace(" ♪", "")
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"^[A-Z]+: ", "", text)

    if text != original_text:
        print(f"Original: {original_text}\nCleaned: {text}\n")
    return text.strip()


def process_files(directory, lang_code):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                item["translation"]["en"] = clean_translation(item["translation"]["en"])
                item["translation"][f"{lang_code}"] = clean_translation(
                    item["translation"][f"{lang_code}"]
                )

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)


LANG_CODE = "es"
DIRECTORY = f"./data/en-{LANG_CODE}"
delete_invalid_translation_files(DIRECTORY, LANG_CODE)
process_files(DIRECTORY, LANG_CODE)
