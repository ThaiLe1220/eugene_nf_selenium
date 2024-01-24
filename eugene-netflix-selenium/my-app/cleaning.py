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


def delete_invalid_translation_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                # Check and delete file if necessary
                for item in data:
                    en = item["translation"]["en"]
                    vi = item["translation"]["vi"]
                    if not en or not vi or en != vi:
                        os.remove(file_path)
                        print(f"Deleted file: {filename}")
                        break  # Exit the loop as we've already deleted the file

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {filename}")
            except PermissionError:
                print(
                    f"Cannot delete file, it's being used by another process: {filename}"
                )


DIRECTORY = "./data/en-vi"
delete_invalid_translation_files(DIRECTORY)