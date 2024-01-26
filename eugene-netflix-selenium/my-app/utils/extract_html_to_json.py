import json
import os

from bs4 import BeautifulSoup


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
            subtitle = process_subtitle(cols[1])

            # Extract translation if it exists
            if len(cols) >= 3:
                translation = cols[2].get_text()
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
            f"../markup/note-{source_lang}-{target_lang}.txt", "a", encoding="utf-8"
        ) as f:
            f.write(f"Failed to extract {file_path}\n")

    # Handle other exceptions, specifically no valid translations
    except ValueError as e:
        print(e)

        # Log the error in a text file
        with open(
            f"../markup/note-{source_lang}-{target_lang}.txt", "a", encoding="utf-8"
        ) as f:
            f.write(f"Failed to extract {file_path}\n")


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
    ("en", "zh"),
    ("en", "vi"),
    ("en", "fr"),
    ("en", "es"),
    ("en", "ja"),
    # ("vi", "en"),
]


# Processing data for each language pair
for source, target in LANG_PAIRS:
    for i in range(0, 1100):
        if i < len(movies_ids):  # Prevent index out of range
            process_and_save_data(movies_ids[i], source, target)
