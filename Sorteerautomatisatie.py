import os
import shutil
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TARGET_URL = input("Welke website wil je de bestanden van ophalen?: ")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, "downloads")
SORT_DIR = os.path.join(SCRIPT_DIR, "sorted")
WANTED_EXTENSIONS = [".doc", ".docx", ".txt", ".png", ".jpg", ".jpeg", ".pdf"]

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(SORT_DIR, exist_ok=True)



chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "directory_upgrade": True
})
#chrome_options.add_argument("--headless")  # Optioneel: zonder GUI

driver = webdriver.Chrome(options=chrome_options)
driver.get(TARGET_URL)

try:
    # Wait up to 10 seconds for the cookie accept button to appear
    accept_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//*[contains(text(),'Accept') or contains(text(),'Consent') or contains(text(),'Accepteren')]"
    ))
)
    accept_button.click()
    print("Cookie banner accepted.")
except Exception as e:
    print("No cookie banner found or error accepting cookies:", e)

# Functie om afbeeldingen te downloaden
def download_image(url, download_dir):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = os.path.basename(url)
            filepath = os.path.join(download_dir, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Afbeelding gedownload: {filename}")
        else:
            print(f"Kon afbeelding niet downloaden: {url} (Status: {response.status_code})")
    except Exception as e:
        print(f"Fout bij downloaden van afbeelding: {e}")

#Alle downloadlinks klikken
download_links = []

# Collect hrefs first
links = driver.find_elements(By.TAG_NAME, "a")
try:
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and any(href.lower().endswith(ext) for ext in WANTED_EXTENSIONS):
            download_links.append(href)

    print(f"Found {len(download_links)} direct download links.")
    print(download_links)

    # alle links afgaan om te downloaden
    for href in download_links:
        if href.lower().endswith((".jpg", ".jpeg", ".png")):
            download_image(href, DOWNLOAD_DIR)
        else:
            driver.get(href)
            print(f"Downloading via Selenium: {href}")
            time.sleep(3)

except StaleElementReferenceException:
    print("Stale element, link skipped.")
except Exception as e:
    print(f"Error processing link: {e}")

# === Wacht op downloads ===
print("Wachten op downloads...")
time.sleep(20)  # Aanpassen indien nodig voor trage downloads


# === Sorteren van bestanden ===
for filename in os.listdir(DOWNLOAD_DIR):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.isfile(filepath):
        ext = os.path.splitext(filename)[1].lower()
        if ext in WANTED_EXTENSIONS:
            # Bepaal submap op type
            if ext in [".png", ".jpg", ".jpeg"]:
                category = "images"
            else:
                category = "documents"

            # Datumfolder aanmaken
            today = datetime.today().strftime("%d-%m-%Y")
            target_folder = os.path.join(SORT_DIR, category, today)
            os.makedirs(target_folder, exist_ok=True)

            # Verplaats bestand
            shutil.move(filepath, os.path.join(target_folder, filename))
            print(f"{filename} verplaatst naar {target_folder}")