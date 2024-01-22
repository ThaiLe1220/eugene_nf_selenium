from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from extract_html import *
import time

options = webdriver.ChromeOptions()
options.add_extension("./extensions/Language-Reactor.crx")
driver = webdriver.Chrome(options=options)

original_tab = driver.current_window_handle
driver.get("https://www.netflix.com/login")
time.sleep(2)

new_tab = [tab for tab in driver.window_handles if tab != original_tab][0]
driver.switch_to.window(new_tab)
driver.close()
driver.switch_to.window(original_tab)

username = "0349087318"
password = "Netfl1x13122000@@&&"

wait = WebDriverWait(driver, 10)
try:
    login_form = wait.until(EC.presence_of_element_located((By.NAME, "userLoginId")))
except Exception as e:
    print(f"Error: {e}")
    exit()

username_field = driver.find_element(By.NAME, "userLoginId")
password_field = driver.find_element(By.NAME, "password")
username_field.send_keys(username)
password_field.send_keys(password)

password_field.send_keys(Keys.RETURN)

wait.until(EC.url_contains("www.netflix.com/browse"))


# Function to read links from a file
def read_links(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


# Function to check links
def check_links(links):
    accessible_links = []
    inaccessible_links = []

    # Check each link
    for link in links:
        try:
            driver.get(link)
            time.sleep(5)  # Wait for page to load; adjust as necessary

            accessible_links.append(link)
        except WebDriverException:
            inaccessible_links.append(link)

    driver.quit()
    return accessible_links, inaccessible_links


# Main
file_path = "../source/movies_links_cleaned.txt"
links = read_links(file_path)
accessible, inaccessible = check_links(links)

print("Accessible Links:", accessible)
print("Inaccessible Links:", inaccessible)
