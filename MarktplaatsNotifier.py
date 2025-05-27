import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# setting options for chrome webdriver
options = Options()
options.add_argument('--headless')  # Headless makes the browser window invisable

driver = webdriver.Chrome(options=options)

def find_elements(elem):

    title = elem.find_element(By.CSS_SELECTOR, "h3.hz-Listing-title").text or "Titel kon niet worden gevonden"

    price = elem.find_element(By.CSS_SELECTOR, "p.hz-Listing-price.hz-Listing-price--mobile.hz-text-price-label").text or "Prijs kon niet worden gevonden"

    bio = elem.find_element(By.CSS_SELECTOR, ".hz-Listing-description").text + "..." or "Beschrijving kon niet worden gevonden"

    img_elem = elem.find_element(By.TAG_NAME, "img")
    image = img_elem.get_attribute("data-src") or img_elem.get_attribute("src") or "Afbeelding-url niet gevonden"

    date = elem.find_element(By.CSS_SELECTOR, "span.hz-Listing-date").text.strip() or "Datum kon niet worden gevonden"

    location = elem.find_element(By.CSS_SELECTOR, "span.hz-Listing-location span.hz-Listing-distance-label").text.strip() or "location kon niet worden gevonden"

    name = elem.find_element(By.CSS_SELECTOR, ".hz-Listing--sellerInfo span.hz-Listing-seller-name-container a span.hz-Listing-seller-name").text.strip() or "Naam kon niet worden gevonden"

    return title, price, image, bio, date, location, name

def get_all_listings(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.hz-Listings")))

    # Search all elements on the page
    elements = driver.find_elements(By.CSS_SELECTOR, "li.hz-Listing.hz-Listing--list-item")
    total = len(elements)
    print(f"Aantal listings gevonden: {total}")

    # For every listing a make beter looking output
    for idx, elem in enumerate(elements, start=1):
        title, price, image, bio, date, location, name = find_elements(elem)
        print(f"\nListing {idx}/{total}:")
        print(f"    Titel       : {title}")
        print(f"    Prijs       : {price}")
        print(f"    Afbeelding  : {image}")
        print(f"    Beschrijving: {bio}")
        print(f"    Datum       : {date}")
        print(f"    Locatie     : {location}")
        print(f"    Verkoper    : {name}")


def main():
    while True:
        try:
            checker_delay = int(input("Hoe vaak wilt u controleren op nieuwe producten? (in seconden): "))
            url = input("Marktplaats profiel url: ")
            get_all_listings(url)
            driver.get(url)
            while True:
                elemts = get_all_listings(url)
                time.sleep(checker_delay)
                new_elem = get_all_listings(url)
                if elemts != new_elem:
                    print("Nieuwe listings gevonden of bestaande listings zijn gewijzigd!")
                    get_all_listings(url)
                else:
                    print("Geen nieuwe listings gevonden.")


        except Exception as e:
            print(f"Root Error: {e}")

        finally:
            driver.quit()

if __name__ == "__main__":
    main()