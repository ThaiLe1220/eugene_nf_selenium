"""Filename: main.py - Directory: ./my-app"""
import os
from bs4 import BeautifulSoup
import time
import os
import re
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def netflix_authenticate(cur_driver, username, password):
    """
    Authenticate a user on Netflix using Selenium.

    This function navigates to the Netflix login page, handles any additional opened tabs,
    and logs in using the provided username and password. It waits for the Netflix
    browse URL to ensure the login was successful.

    Args:
        cur_driver (webdriver): The Selenium WebDriver instance being used for automation.
        username (str): The username or email for the Netflix account.
        password (str): The password for the Netflix account.
    """

    print(" [ netflix_authenticate() ] ", end="")
    cur_driver.get("https://www.netflix.com/login")
    time.sleep(1)
    if len(cur_driver.window_handles) > 1:
        new_tab = [
            tab
            for tab in cur_driver.window_handles
            if tab != cur_driver.current_window_handle
        ][0]
        cur_driver.switch_to.window(new_tab)
        cur_driver.close()
        cur_driver.switch_to.window(cur_driver.window_handles[0])
    time.sleep(5)
    username_field = cur_driver.find_element(By.NAME, "userLoginId")
    password_field = cur_driver.find_element(By.NAME, "password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    wait.until(EC.url_contains("www.netflix.com/browse"))
    time.sleep(1)


def click_setting_button(cur_wait):
    """
    Click the settings button on a webpage using Selenium.

    Waits until the settings button is clickable on the current page, and then clicks it.
    This function is specifically designed to interact with elements matching a certain
    CSS selector, presumably in a specific web application or webpage.

    Args:
        cur_wait (WebDriverWait): The WebDriverWait instance used for handling wait conditions.
    """

    print(" [ click_setting_button() ] ", end="")
    settings_button = cur_wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".lln-vv-toolbar-btn.lln-vv-top-btn.tippy.lln-vv-options-btn",
            )
        )
    )
    settings_button.click()


def close_all_tabs(cur_driver):
    """
    Close all browser tabs except the first one using Selenium.

    Iterates through all open browser tabs, closes each one except for the first tab,
    and then switches back to the first tab. This function is useful for cleanup
    during a web scraping or web automation task.

    Args:
        cur_driver (webdriver): The Selenium WebDriver instance being used for automation.
    """

    print(" [ close_all_tabs() ] ", end="")
    all_handles = cur_driver.window_handles
    cur_driver.switch_to.window(all_handles[0])
    for handle in all_handles[1:]:
        cur_driver.switch_to.window(handle)
        cur_driver.close()
    cur_driver.switch_to.window(all_handles[0])
    time.sleep(0.5)


def choose_language_translation(cur_driver, cur_wait, language):
    """
    Chooses a specified language for translation on a web page using Selenium.

    This function locates and clicks on the translation language dropdown on a web page,
    waits for the dropdown options to be visible, and then selects the specified language.
    It's tailored for web pages where translations are available and language can be selected
    through a dropdown menu.

    Args:
        cur_driver (webdriver): The Selenium WebDriver instance used for web automation.
        cur_wait (WebDriverWait): The WebDriverWait instance used for handling wait conditions.
        language (str): The language to be selected for translation.
    """

    print(f" [ choose_language_translation() for {language} ] ", end="")
    translation_language_dropdown = cur_wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//span[contains(text(), 'Translation language')]/following-sibling::span//span[@class='select2-selection select2-selection--single']",
            )
        )
    )
    translation_language_dropdown.click()

    # After clicking the dropdown, wait for the dropdown options to appear
    cur_wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".select2-results__options"))
    )
    language_option = cur_driver.find_element(
        By.XPATH, f"//li[contains(., '{language}')]"
    )
    actions = ActionChains(cur_driver)
    actions.move_to_element(language_option).perform()
    language_option.click()


def choose_export_machine_translation(cur_driver):
    """
    Selects the option to include machine translations during export.

    This function finds and clicks a checkbox on a web page that allows the inclusion of
    machine translations in an exported document. It's specifically designed for pages
    where such an option exists.

    Args:
        cur_driver (webdriver): The Selenium WebDriver instance used for web automation.
    """

    print(" [ choose_export_machine_translation() ] ", end="")
    mt_checkbox = cur_driver.find_element(
        By.CSS_SELECTOR, "input[type='checkbox'][name='includeMachineTranslations']"
    )
    mt_checkbox.click()
    time.sleep(1)


def close_setting_button(cur_driver):
    """
    Closes the settings modal/dialog on a web page using Selenium.

    Finds and executes a script to click the close button of a settings modal or dialog.
    This function is useful for web pages where standard click actions might not work
    on certain elements due to overlapping layers or other UI complexities.

    Args:
        cur_driver (webdriver): The Selenium WebDriver instance used for web automation.
    """

    print(" [ close_setting_button() ] ", end="")
    settings_button = cur_driver.find_element(
        By.CSS_SELECTOR, ".lln-close-modal.lln-close-modal-btn"
    )
    cur_driver.execute_script("arguments[0].click();", settings_button)


def export_translation(cur_driver, cur_wait, index, lang_code):
    """
    Exports the translation of a Netflix show or movie's page to an HTML file.

    This function clicks the export button on a web page (presumably a Netflix page with the Language Reactor extension), waits for and clicks the export option, and then saves the page source to an HTML file. It handles multiple browser windows if they are opened during the process.

    Args:
        cur_driver (webdriver): The Selenium WebDriver instance used for automation.
        cur_wait (WebDriverWait): The WebDriverWait instance used for handling wait conditions.
        index (int): The index of the current movie or show in a list, used to name the output file.
        lang_code (str): The language code representing the translation language, used in the output file name.
    """

    print(" [ export_translation() ] ", end="")
    export_button = cur_wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".lln-vv-toolbar-btn.lln-vv-top-btn.lln-open-export-modal.tippy",
            )
        )
    )
    export_button.click()

    export_option = cur_wait.until(
        EC.element_to_be_clickable((By.ID, "llnExportModalExportBtn"))
    )
    export_option.click()
    time.sleep(1)

    if len(cur_driver.window_handles) > 1:
        new_tab = [
            tab
            for tab in cur_driver.window_handles
            if tab != cur_driver.current_window_handle
        ][0]
        cur_driver.switch_to.window(new_tab)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract the first table row (header row)
        first_row = soup.find("tr")

        # Check if the first row has a column for 'Translation'
        has_translation_column = "Translation" in first_row.get_text()

        if has_translation_column:
            filename = f"./markup/en-{lang_code}/{MOVIE_IDS[index]}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(page_source)

            print(f"\nThe HTML of the page has been saved as {filename}")
        else:
            print("No translation, skipping file")
            with open(
                f"./source/movies_links_en_{LANGUAGE_CODE}_no_translation.txt",
                "a",
                encoding="utf-8",
            ) as f:
                f.write(link + "\n")


def clean_netflix_links(input_file, output_file):
    """
    Cleans and sorts Netflix links from an input file and writes them to an output file.

    Reads Netflix links from the specified input file, extracts and cleans the movie or show IDs
    from these links, and then writes the cleaned and sorted unique links to the specified output file.
    This function is useful for preprocessing a list of Netflix URLs.

    Args:
        input_file (str): The path to the file containing the original Netflix links.
        output_file (str): The path to the file where the cleaned and sorted links will be saved.
    """
    print(" [ clean_netflix_links() ] ")

    cleaned_links = []

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("https://www.netflix.com/watch/"):
                movie_id = re.split(r"[^0-9]", line.split("/")[-1])[0]
                cleaned_link = f"https://www.netflix.com/watch/{movie_id}"
                cleaned_links.append(cleaned_link)

    sorted_links = sorted(cleaned_links, key=lambda x: int(x.split("/")[-1]))
    unique_sorted_links = sorted(set(link.strip() for link in sorted_links))

    with open(output_file, "w", encoding="utf-8") as file:
        for link in unique_sorted_links:
            file.write(link + "\n")


load_dotenv()

LANG_LIST = [
    ("Vietnamese", "vi"),
    ("Spanish", "es"),
    ("English", "en"),
    ("French", "fr"),
    ("German", "de"),
    ("Italian", "it"),
    ("Korean", "ko"),
    ("Japanese", "ja"),
    ("Chinese (Simplified)", "zh"),
    ("Portuguese", "pt"),
    ("Thai", "th"),
    ("Russian", "th"),
]
START_INDEX = 0
END_INDEX = 1100

LANGUAGE = "Italian"
LANGUAGE_CODE = {name: code for name, code in LANG_LIST}.get(LANGUAGE)
NETFLIX_LINKS = []
MOVIE_IDS = []

# Read and process Netflix links from a file
with open("./source/movies_links_cleaned.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line.startswith("https://www.netflix.com/watch/"):
            NETFLIX_LINKS.append(line)
            movie_id = line.split("/")[-1]
            MOVIE_IDS.append(movie_id)


# Initialize Selenium WebDriver with Chrome options (extensions)
options = webdriver.ChromeOptions()
options.add_extension("./extensions/Language-Reactor.crx")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# Authenticate on Netflix
netflix_authenticate(driver, os.getenv("NF_USERNAME"), os.getenv("NF_PASSWORD"))

# Iterate over the list of Netflix links
for i, link in enumerate(NETFLIX_LINKS):
    if START_INDEX <= i <= END_INDEX:
        start_time = time.time()
        file_path = f"./markup/en-{LANGUAGE_CODE}/{MOVIE_IDS[i]}.html"

        # Check if the file exists
        if os.path.exists(file_path):
            # Read the HTML content from the file
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract the first table row (header row)
            first_row = soup.find("tr")

            # Check if the first row has a column for 'Translation'
            has_translation_column = "Translation" in first_row.get_text()

            if has_translation_column:
                print(f"Skipping already processed movie: {MOVIE_IDS[i]}")
                START_INDEX += 1
                continue  # Skip this movie as it has been processed
            else:
                print(f"Invalid markup detected, reprocessing movie: {MOVIE_IDS[i]}")

        driver.get(link)

        try:
            if i == START_INDEX:
                # Setting up the translation options only for the first link
                click_setting_button(wait)
                choose_language_translation(driver, wait, LANGUAGE)
                time.sleep(1)
                close_setting_button(driver)
                time.sleep(1)

            # Wait for subtitles to load
            wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".lln-vertical-view-sub.lln-sentence-wrap.lln-with-play-btn.odd.in-scroll",
                    )
                )
            )

            # Export the translation
            export_translation(driver, wait, i, LANGUAGE_CODE)
            close_all_tabs(driver)

        except WebDriverException:
            print(f"{link} Inaccessible")
            with open(
                f"./source/movies_links_en_{LANGUAGE_CODE}_inaccessed.txt",
                "a",
                encoding="utf-8",
            ) as file:
                file.write(link + "\n")

        elapsed_time = time.time() - start_time
        print(
            f"Time taken for iteration {i}, film {MOVIE_IDS[i]}, translation en-{LANGUAGE_CODE}: {elapsed_time:.2f} seconds"
        )


# Clean list of inaccessed Netflix links
clean_netflix_links(
    f"./source/movies_links_en_{LANGUAGE_CODE}_inaccessed.txt",
    f"./source/movies_links_en_{LANGUAGE_CODE}_inaccessed.txt",
)

# Close the WebDriver
driver.quit()
