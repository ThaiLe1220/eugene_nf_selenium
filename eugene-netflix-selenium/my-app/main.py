"""Filename: main.py - Directory: ./my-app"""

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


def google_authenticate(cur_driver, username, password):
    print(" [ google_authenticate() ] ", end="")
    cur_driver.get(
        "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%3Futm_source%3Daccount-marketing-page%26utm_medium%3Dgo-to-account-button&ifkv=ASKXGp2ElErrlp6KI4Coxg5NIA00uJNFj2s1WJiy5hUdDcMorxOJm5AZa_RgOe8x0MyvF-Uwk56RNQ&service=accountsettings&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-854968125%3A1705915296809620&theme=glif"
    )
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
        time.sleep(1)
        # email_field = cur_driver.find_element(By.ID, "identifierId")
        # email_field.click()
        # email_field.send_keys(username)
        # email_field.send_keys(Keys.RETURN)
        # time.sleep(4)
        # password_field = cur_driver.find_element(By.NAME, "Passwd")
        # password_field.send_keys(password)
        # password_field.send_keys(Keys.RETURN)
        # time.sleep(3)
    time.sleep(1)


def netflix_authenticate(cur_driver, username, password):
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
    print(" [ close_all_tabs() ] ", end="")
    all_handles = cur_driver.window_handles
    cur_driver.switch_to.window(all_handles[0])
    for handle in all_handles[1:]:
        cur_driver.switch_to.window(handle)
        cur_driver.close()
    cur_driver.switch_to.window(all_handles[0])
    time.sleep(0.5)


def extension_sign_in(cur_driver, cur_wait):
    print(" [ extension_sign_in() ] ", end="")
    time.sleep(2)
    sign_in_button = cur_wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".lln-red-button.lln-btn-start-loud-login")
        )
    )
    sign_in_button.click()
    time.sleep(5)
    if len(cur_driver.window_handles) > 1:
        new_tab = [
            tab
            for tab in cur_driver.window_handles
            if tab != cur_driver.current_window_handle
        ][0]
        cur_driver.switch_to.window(new_tab)
        main_window_handle = cur_driver.current_window_handle

        cur_wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".firebaseui-idp-button.mdl-button.mdl-js-button.mdl-button--raised.firebaseui-idp-google.firebaseui-id-idp-button",
                )
            )
        )
        gg_login_button = cur_driver.find_element(
            By.CSS_SELECTOR,
            ".firebaseui-idp-button.mdl-button.mdl-js-button.mdl-button--raised.firebaseui-idp-google.firebaseui-id-idp-button",
        )

        gg_login_button.click()
        time.sleep(4)
        time.sleep(10)
        for handle in cur_driver.window_handles:
            if handle != main_window_handle:
                cur_driver.switch_to.window(handle)
        # time.sleep(3)
        # email_select = cur_driver.find_element(By.CSS_SELECTOR, ".WBW9sf")
        # email_select.click()
        # time.sleep(3)

    cur_driver.switch_to.window(main_window_handle)
    time.sleep(5)


def choose_language_translation(cur_driver, cur_wait, language):
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


def choose_machine_translation(cur_driver):
    print(" [ choose_machine_translation() ] ", end="")
    mt_checkbox = cur_driver.find_element(By.ID, "showMT")
    actions = ActionChains(cur_driver)
    actions.move_to_element(mt_checkbox).perform()
    mt_checkbox.click()
    time.sleep(1)


def choose_export_machine_translation(cur_driver):
    print(" [ choose_export_machine_translation() ] ", end="")
    mt_checkbox = cur_driver.find_element(
        By.CSS_SELECTOR, "input[type='checkbox'][name='includeMachineTranslations']"
    )
    mt_checkbox.click()
    time.sleep(1)


def close_setting_button(cur_driver):
    print(" [ close_setting_button() ] ", end="")
    settings_button = cur_driver.find_element(
        By.CSS_SELECTOR, ".lln-close-modal.lln-close-modal-btn"
    )
    cur_driver.execute_script("arguments[0].click();", settings_button)


def export_translation(cur_driver, cur_wait, index, lang_code):
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

    # time.sleep(1)
    # choose_export_machine_translation(cur_driver)
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
        filename = f"./markup/en-{lang_code}/{MOVIE_IDS[index]}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(page_source)

        print(f"\nThe HTML of the page has been saved as {filename}")


def clean_NETFLIX_LINKS(input_file, output_file):
    cleaned_links = []

    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("https://www.netflix.com/watch/"):
                movie_id = re.split(r"[^0-9]", line.split("/")[-1])[0]
                cleaned_link = f"https://www.netflix.com/watch/{movie_id}"
                cleaned_links.append(cleaned_link)

    sorted_links = sorted(cleaned_links, key=lambda x: int(x.split("/")[-1]))
    unique_sorted_links = sorted(set(link.strip() for link in sorted_links))

    with open(output_file, "w") as file:
        for link in unique_sorted_links:
            file.write(link + "\n")


load_dotenv()

lang_list = [
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

START_INDEX = 105
END_INDEX = 115
LANGUAGE = "French"
LANGUAGE_CODE = {name: code for name, code in lang_list}.get(LANGUAGE)

options = webdriver.ChromeOptions()
options.add_extension("./extensions/Language-Reactor.crx")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# google_authenticate(driver, os.getenv("GG_USERNAME"), os.getenv("GG_PASSWORD"))
netflix_authenticate(driver, os.getenv("NF_USERNAME"), os.getenv("NF_PASSWORD"))

NETFLIX_LINKS = []
MOVIE_IDS = []

with open("./source/movies_links_cleaned.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line.startswith("https://www.netflix.com/watch/"):
            NETFLIX_LINKS.append(line)
            movie_id = line.split("/")[-1]
            MOVIE_IDS.append(movie_id)

#<<<<<<< HEAD
for i, link in enumerate(netflix_links):
    start_index = 0
    end_index = 1092
#=======
for i, link in enumerate(NETFLIX_LINKS):
    if START_INDEX <= i <= END_INDEX:
        start_time = time.time()
        driver.get(link)
#>>>>>>> fa4f5da485623af5927209de33146c6f94f79590

        try:
            if i == START_INDEX:
                click_setting_button(wait)
                # extension_sign_in(driver, wait)
                # driver.switch_to.window(driver.window_handles[0])
#<<<<<<< HEAD
                choose_language_translation(driver, wait, "French")
#=======
                choose_language_translation(driver, wait, LANGUAGE)
                time.sleep(1)
#>>>>>>> fa4f5da485623af5927209de33146c6f94f79590
                # choose_machine_translation(driver)
                close_setting_button(driver)
                time.sleep(1)

#<<<<<<< HEAD
            export_translation(driver, wait, i, "French")
#=======
            wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".lln-vertical-view-sub.lln-sentence-wrap.lln-with-play-btn.odd.in-scroll",
                    )
                )
            )
            export_translation(driver, wait, i, LANGUAGE_CODE)
#>>>>>>> fa4f5da485623af5927209de33146c6f94f79590
            close_all_tabs(driver)

        except WebDriverException:
            print(f"{link} Inaccessible")
            with open(
                f"./source/movies_links_en_{LANGUAGE_CODE}_inaccessed.txt",
                "a",
                encoding="utf-8",
            ) as file:
                file.write(link + "\n")

        elapsed_time = time.time() - start_time  # Calculate elapsed time
        print(
            f"Time taken for iteration {i}, film {MOVIE_IDS[i]}, translation en-{LANGUAGE_CODE}: {elapsed_time:.2f} seconds"
        )


clean_NETFLIX_LINKS(
    f"./source/movies_links_en_{LANGUAGE_CODE}_inaccessed.txt",
    f"./source/movies_links_en_{LANGUAGE_CODE}_inaccessed.txt",
)

driver.quit()
