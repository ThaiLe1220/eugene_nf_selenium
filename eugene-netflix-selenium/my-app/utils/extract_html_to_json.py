import json
import os
import re
from bs4 import BeautifulSoup


def delete_invalid_translation_files(lang_code):
    """_summary_

    Args:
        lang_code (_type_): _description_
    """

    print(f" [ delete_invalid_translation_files() {lang_code}] ")
    directory = f"../data/en-{target}"

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


def clean_netflix_links(input_file, output_file):
    """
    Cleans and sorts Netflix links from an input file and writes them to an output file.

    Reads Netflix links from the specified input file, extracts and cleans the movie or show IDs from these links, and then writes the cleaned and sorted unique links to the specified output file. This function is useful for preprocessing a list of Netflix URLs.

    Args:
        input_file (str): The path to the file containing the original Netflix links.
        output_file (str): The path to the file where the cleaned and sorted links will be saved.
    """
    print(f" [ clean_netflix_links() {input_file}] ")

    cleaned_links = []

    with open(input_file, "r", encoding="utf-8") as file:
        for link in file:
            link = link.strip()
            if link.startswith("https://www.netflix.com/watch/"):
                movie_id = re.split(r"[^0-9]", link.split("/")[-1])[0]
                cleaned_link = f"https://www.netflix.com/watch/{movie_id}"
                cleaned_links.append(cleaned_link)

    sorted_links = sorted(cleaned_links, key=lambda x: int(x.split("/")[-1]))
    unique_sorted_links = sorted(set(link.strip() for link in sorted_links))

    with open(output_file, "w", encoding="utf-8") as file:
        for link in unique_sorted_links:
            file.write(link + "\n")


def clean_text(text):
    text = text.replace("\n", "")
    text = text.replace("\u200E", "")

    return text.strip()


def process_subtitle(td):
    """Processes a table data element to extract and concatenate subtitles.

    Args:
        td (bs4.element.Tag): A BeautifulSoup Tag object representing a table data element.

    Returns:
        str: A concatenated string of subtitles.
    """

    processed_subtitle = ""

    # Iterate over children of the table data element
    for element in td.children:
        # Process only 'span' elements which contain the subtitle text
        if element.name == "span":
            text = element.get_text()
            processed_subtitle += text + ""

    return processed_subtitle


def process_and_save_data(movies_id, source_lang, target_lang):
    """Processes HTML content to extract subtitle translations and saves them as JSON.

    Args:
        movies_id (str): Identifier for the movie.
        source_lang (str): Source language code.
        target_lang (str): Target language code.

    Raises:
        ValueError: If no valid translations are found for the given movie ID.
    """

    print(f" process_and_save_data() {movies_id} {source_lang}-{target_lang}")
    file_path = f"../markup/{source_lang}-{target_lang}/{movies_id}.html"

    try:
        # Read the HTML content from the specified file
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract all table rows (skipping the header row)
        rows = soup.find_all("tr")[1:]

        translations = []
        # Process each row to extract subtitles and translations
        for row in rows:
            cols = row.find_all("td")
            subtitle = clean_text(process_subtitle(cols[1]))
            # Extract translation if it exists
            if len(cols) >= 3:
                translation = clean_text(cols[2].get_text())
            else:
                translation = ""

            # Append to translations list if both subtitle and translation are valid and not identical
            if subtitle and translation and subtitle != translation:
                translations.append(
                    {
                        "translation": {
                            f"{source_lang}": subtitle,
                            f"{target_lang}": translation,
                        }
                    }
                )

        # Raise an error if no valid translations are found
        if not translations:
            raise ValueError(f"No valid translations found for {movies_id}")

        # Create directory for saving data, if it doesn't exist
        dir_path = f"../data/{source_lang}-{target_lang}"
        os.makedirs(dir_path, exist_ok=True)

        # Save the extracted translations to a JSON file
        with open(
            f"../data/{source_lang}-{target_lang}/{movies_id}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(translations, f, indent=2, ensure_ascii=False)
            print(
                f"The subtitle has been saved as ../data/{source_lang}-{target_lang}/{movies_id}.json"
            )

    # Handle file not found error
    except FileNotFoundError:
        print(f"File not found: {file_path}")

        # Log the file not found error in a text file
        with open(
            f"../markup/{source_lang}-{target_lang}-invalid-html.txt",
            "a",
            encoding="utf-8",
        ) as f:
            f.write(f"https://www.netflix.com/watch/{movie_id}\n")

    # Handle other exceptions, specifically no valid translations
    except ValueError as e:
        print(e)

        # Log the error in a text file
        with open(
            f"../markup/{source_lang}-{target_lang}-invalid-html.txt",
            "a",
            encoding="utf-8",
        ) as f:
            f.write(f"https://www.netflix.com/watch/{movie_id}\n")


# Initialize lists to store Netflix movie links and their corresponding IDs
netflix_links = []
movies_ids = []

# Read and process cleaned Netflix movie links
with open("../source/movies_links_cleaned.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line.startswith("https://www.netflix.com/watch/"):
            netflix_links.append(line)
            movie_id = line.split("/")[-1]
            movies_ids.append(movie_id)


# Define language pairs for processing
LANG_PAIRS = [
    # ("en", "vi"),
    # ("en", "es"),
    ("en", "zh"),
    ("en", "fr"),
    ("en", "ja"),
]


# Processing data for each language pair
for source, target in LANG_PAIRS:
    for i in range(20, 1100):
        print(f"Iteration {i}: ", end="")
        if i < len(movies_ids):  # Prevent index out of range
            process_and_save_data(movies_ids[i], source, target)

    delete_invalid_translation_files(target)
    invalid_html_directory = f"../markup/{source}-{target}-invalid-html.txt"
    clean_netflix_links(invalid_html_directory, invalid_html_directory)
