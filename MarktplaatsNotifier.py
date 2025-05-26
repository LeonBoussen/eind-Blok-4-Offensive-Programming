from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# setting options for chrome webdriver
options = Options()
options.add_argument('--headless')  # Headless makes the browser window invisable

driver = webdriver.Chrome(options=options)

try:
    url = input("Marktplaats profiel url: ")
    driver.get(url)

    # Wait until elements - Max 10 sec 
    driver.implicitly_wait(10)  

    # Search all elements on the page
    elements = driver.find_elements(By.CSS_SELECTOR, "li.hz-Listing.hz-Listing--list-item")
    totaal = len(elements)
    print(f"Aantal listings gevonden: {totaal}")

    # For every listing a make beter looking output
    for idx, elem in enumerate(elements, start=1):
        # Titel
        titel = elem.find_element(By.CSS_SELECTOR, "h3.hz-Listing-title").text
        prijs = elem.find_element(By.CSS_SELECTOR, ".hz-Listing-price--desktop").text
        beschrijving = elem.find_element(By.CSS_SELECTOR, ".hz-Listing-description").text

        #if it can find date / location add that other wise "onbekend"
        try:
            datum = elem.find_element(By.CSS_SELECTOR, ".hz-Listing-date--desktop").text
        except:
            datum = "Onbekend"
        try:
            locatie = elem.find_element(By.CSS_SELECTOR, ".hz-Listing-location .hz-Listing-distance-label").text
        except:
            locatie = "Onbekend"

        print(f"\nListing {idx}/{totaal}:")
        print(f"    Titel       : {titel}")
        print(f"    Prijs       : {prijs}")
        print(f"    Beschrijving: {beschrijving}")
        print(f"    Datum       : {datum}")
        print(f"    Locatie     : {locatie}")

except Exception as e:
    print(f"Root Error: {e}")

finally:
    driver.quit()
