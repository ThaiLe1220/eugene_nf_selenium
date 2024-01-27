import os
from bs4 import BeautifulSoup

# Initialize counters
counters = {
    'successful_scrapes': 0,
    'missing_translations': 0,
    'not_scraped': 0
}

def has_valid_translations(html_file_path):
    """Check if the HTML file has valid translations.

    Args:
        html_file_path (str): Path to the HTML file.

    Returns:
        bool: True if valid translations are found, False otherwise.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

          # Find the first row of the table, which should contain the headers
        header_row = soup.find("tr")
        if header_row:
            # Find all the spans with class 'table-header' and check if any contain the text 'Translation'
            headers = header_row.find_all("span", class_="table-header")
            for header in headers:
                if 'translation' in header.get_text(strip=True).lower():
                    return True  # Found the 'Translation' column
        return False  # 'Translation' column not found

    except FileNotFoundError:
        return False

def check_and_delete_invalid_html(movie_id, source_lang, target_lang):
    """Check HTML file for accessibility and valid translations, and delete if invalid.

    Args:
        movie_id (str): Identifier for the movie.
        source_lang (str): Source language code.
        target_lang (str): Target language code.
    """
    html_file_path = f"../markup/{source_lang}-{target_lang}/{movie_id}.html"
    error_log_file = f"../source/HTML_{source_lang}_{target_lang}_errors_deleted.txt"

    # Check if HTML file exists and has valid translations
   # Check if HTML file exists
    if not os.path.exists(html_file_path):
        print(f"HTML file does not exist: {html_file_path}")

        counters['not_scraped'] += 1
    elif not has_valid_translations(html_file_path):
        print(f"Missing 'Translation' column: {html_file_path}")
        os.remove(html_file_path)
        print(f"Deleted invalid HTML file: {html_file_path}")
        with open(error_log_file, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Deleted invalid HTML file: {html_file_path}\n")
        counters['missing_translations'] += 1
    else:
        print(f"Successfully scraped HTML file: {html_file_path}")
        counters['successful_scrapes'] += 1

# Initialize lists to store Netflix movie links and their corresponding IDs
netflix_links = []
movies_ids = []

# Define language pairs for processing
LANG_PAIRS = [
    ("en", "th"),
    # ... [Other language pairs]
]

# Read and process cleaned Netflix movie links
with open("../source/movies_links_cleaned.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line.startswith("https://www.netflix.com/watch/"):
            netflix_links.append(line)
            movie_id = line.split("/")[-1]
            movies_ids.append(movie_id)

print(f"Processing for language pairs: {LANG_PAIRS}")
print(f"Number of movies to process: {len(movies_ids)}")

# Processing data for each language pair
for source, target in LANG_PAIRS:
    for i, movie_id in enumerate(movies_ids):
        print(f"Processing {i + 1}/{len(movies_ids)}: {movie_id}")
        check_and_delete_invalid_html(movie_id, source, target)

print("Script completed.")
print(f"Number of successful scrapes: {counters['successful_scrapes']}")
print(f"Number of HTML files with missing translations: {counters['missing_translations']}")
print(f"Number of movie IDs not scraped to HTML: {counters['not_scraped']}")