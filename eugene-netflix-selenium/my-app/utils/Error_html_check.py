import os
from bs4 import BeautifulSoup

# Initialize counters
counters = {
    'en_th': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0},
    'en_vi': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0},
    'en_es': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0},
    'en_de': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0},
    'en_fr': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0},
    'en_it': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0},
    'en_ja': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0},
    'en_ko': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0},
    'en_zh': {'successful_scrapes': 0, 'missing_translations': 0, 'not_scraped': 0}
}

# Initialize overall counters
overall_counters = {
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
    lang_pair_key = f"{source_lang}_{target_lang}"
    html_file_path = f"../markup/{source_lang}-{target_lang}/{movie_id}.html"
    error_log_file = f"../source/HTML_{source_lang}_{target_lang}_errors_deleted.txt"

    # Check if HTML file exists and has valid translations
   # Check if HTML file exists
    if not os.path.exists(html_file_path):
        print(f"HTML file does not exist: {html_file_path}")
        counters[lang_pair_key]['not_scraped'] += 1 
        overall_counters['not_scraped'] += 1
    elif not has_valid_translations(html_file_path):
        print(f"Missing 'Translation' column: {html_file_path}")
        # os.remove(html_file_path) -- Commented out to prevent accidental deletion
        print(f"Deleted invalid HTML file: {html_file_path}")
        with open(error_log_file, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Deleted invalid HTML file: {html_file_path}\n")
        counters[lang_pair_key]['missing_translations']  += 1
        overall_counters['missing_translations'] += 1
    else:
        print(f"Successfully scraped HTML file: {html_file_path}")
        overall_counters['successful_scrapes'] += 1
        counters[lang_pair_key]['successful_scrapes']  += 1

# Initialize lists to store Netflix movie links and their corresponding IDs
netflix_links = []
movies_ids = []

# Define language pairs for processing
LANG_PAIRS = [
    ("en", "th"),
    ("en", "vi"),
    ("en", "es"),
    ("en", "de"),
    ("en", "fr"),
    ("en", "it"),
    ("en", "ja"),
    ("en", "ko"),
    ("en", "zh"),
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

# Processing data for each language pair
for source, target in LANG_PAIRS:
    print('-------------------------------------------------------------')
    print(f"Processing language pair: {source}-{target}")
   
    # for i, movie_id in enumerate(movies_ids):
    # for i, movie_id in enumerate(movies_ids[:10]):
    for i, movie_id in enumerate(movies_ids):
        print(f"Processing {i + 1}/{len(movies_ids)}: {movie_id}")
        check_and_delete_invalid_html(movie_id, source, target)
        
        # Calculate overall success and failure rate
        # total_movies = len(movies_ids[:10]) * 9
        total_movies = len(movies_ids) * 9
        overall_success_rate = (overall_counters['successful_scrapes'] / total_movies) * 100
        overall_failure_rate = 100 - overall_success_rate
                
    # Create log files for each language pair
    # Create log file for the current language pair
    lang_pair = f"{source}_{target}"
    lang_counters = counters[lang_pair]
    # total_movies = len(movies_ids[:10])
    total_movies = len(movies_ids)
    success_rate = (counters[lang_pair]['successful_scrapes'] / total_movies) * 100
    failure_rate = 100 - success_rate
    log_file_path = f"../Performance/HTML_{lang_pair}_performance_log.txt"
    print('-------------------------------------------------------------')
    print(f"Performance of {lang_pair}")
    print(f"Number of successful scrapes: {counters[lang_pair]['successful_scrapes']}")
    print(f"Number of HTML files with missing translations: {counters[lang_pair]['missing_translations']}")
    print(f"Number of movie IDs not scraped to HTML: {counters[lang_pair]['not_scraped']}")
    print(f"Success rate of {lang_pair}: {success_rate:.2f}%")
    print(f"Failure rate of {lang_pair}: {failure_rate:.2f}%")
    print(f"Script of {lang_pair} completed.")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write(f"Number of successful scrapes: {lang_counters['successful_scrapes']}\n")
        log_file.write(f"Number of HTML files with missing translations: {lang_counters['missing_translations']}\n")
        log_file.write(f"Number of movie IDs not scraped to HTML: {lang_counters['not_scraped']}\n")
        log_file.write(f"Success rate of {lang_pair}: {success_rate}%\n")      

# Write overall results to log file
overall_log_file_path = "../Performance/HTML_overall_performance_log.txt"
with open(overall_log_file_path, 'w', encoding='utf-8') as overall_log_file:
    overall_log_file.write(f"Overall number of successful scrapes: {overall_counters['successful_scrapes']}\n")
    overall_log_file.write(f"Overall number of HTML files with missing translations: {overall_counters['missing_translations']}\n")
    overall_log_file.write(f"Overall number of movie IDs not scraped to HTML: {overall_counters['not_scraped']}\n")
    overall_log_file.write(f"Overall success rate: {overall_success_rate}%\n")
    overall_log_file.write(f"Overall failure rate: {overall_failure_rate}%\n")

# Print overall counters
print('-------------------------------------------------------------')
print('Overall Counters:')
print(f"Successful Scrapes: {overall_counters['successful_scrapes']}")
print(f"Missing Translations: {overall_counters['missing_translations']}")
print(f"Not Scraped: {overall_counters['not_scraped']}")
print(f"Overall Success Rate: {overall_success_rate:.2f}%")
print(f"Overall Failure Rate: {overall_failure_rate:.2f}%")
