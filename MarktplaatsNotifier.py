import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# setting options for chrome webdriver
options = Options()
options.add_argument('--headless')  # Headless maakt het browservenster onzichtbaar
options.add_argument("--log-level=2") # print alleen error logs
options
driver = webdriver.Chrome(options=options)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("Press Enter to continue...")

def find_elements(elem): # make var and set value to element named or else return default value
    title = elem.find_element(By.CSS_SELECTOR, "h3.hz-Listing-title").text or "Titel kon niet worden gevonden"
    price = elem.find_element(By.CSS_SELECTOR, "p.hz-Listing-price.hz-Listing-price--mobile.hz-text-price-label").text or "Prijs kon niet worden gevonden"
    bio = elem.find_element(By.CSS_SELECTOR, ".hz-Listing-description").text + "..." or "Beschrijving kon niet worden gevonden"
    img_elem = elem.find_element(By.TAG_NAME, "img")
    image = img_elem.get_attribute("data-src") or img_elem.get_attribute("src") or "Afbeelding-url niet gevonden"
    date = elem.find_element(By.CSS_SELECTOR, "span.hz-Listing-date").text.strip() or "Datum kon niet worden gevonden"
    location = elem.find_element(By.CSS_SELECTOR, "span.hz-Listing-location span.hz-Listing-distance-label").text.strip() or "Locatie kon niet worden gevonden"
    name = elem.find_element(By.CSS_SELECTOR, ".hz-Listing--sellerInfo span.hz-Listing-seller-name-container a span.hz-Listing-seller-name").text.strip() or "Naam kon niet worden gevonden"
    return title, price, image, bio, date, location, name

def get_all_listings(url, print_output=True):
    # Load the URL in browser
    driver.get(url)
    # Wait until the listings element is loaded in the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.hz-Listings"))
    )

    # Find all listing elements on the page
    elements = driver.find_elements(By.CSS_SELECTOR, "li.hz-Listing.hz-Listing--list-item")
    data_list = []
    total = len(elements)
    if print_output:
        print(f"Aantal listings gevonden: {total}")

    # Extract data from each listing element and store it in a list
    for idx, elem in enumerate(elements, start=1):
        title, price, image, bio, date, location, name = find_elements(elem)
        listing_data = {
            "title": title,
            "price": price,
            "image": image,
            "bio": bio,
            "date": date,
            "location": location,
            "name": name,
        }
        data_list.append(listing_data)

        # Optionally print the listing details
        if print_output:
            print(f"\nListing {idx}/{total}:")
            print(f"    Titel       : {title}")
            print(f"    Prijs       : {price}")
            print(f"    Afbeelding  : {image}")
            print(f"    Beschrijving: {bio}")
            print(f"    Datum       : {date}")
            print(f"    Locatie     : {location}")
            print(f"    Verkoper    : {name}")

    # Return the list of all extracted listings
    return data_list

def main():
    while True:
        try:
            try:
                checker_delay = int(input("Hoe vaak moet de profiel gechecked worden voor veranderingen (in seconden | 5 sec default): ") or 5)
            # value error handling for ! int or ints < 1
            except ValueError or checker_delay < 1:
                print("invalid input, using default value of 5 seconds.")
                checker_delay = 5

            
            url = input("Marktplaats profiel url: ")

            # Get initial data from profile to check for changes
            previous_listings = get_all_listings(url)

            # main checking loop
            while True:
                # make new requests of the profile data
                new_listings = get_all_listings(url, print_output=False)

                # check if the old listings are different from the new listings
                if previous_listings != new_listings:
                    clear()
                    print("Nieuwe listings gevonden of bestaande listings zijn gewijzigd!")
                    # calculate the differences
                    min_len = min(len(previous_listings), len(new_listings))
                    
                    # loop through all listings up to the minimum length to check what item changed
                    for idx in range(min_len):
                        old = previous_listings[idx]
                        new = new_listings[idx]

                        # if a change is detected in the listing print the changes
                        if old != new:
                            print(f"\nListing {idx+1} gewijzigd:")
                            for key in old:
                                if old[key] != new[key]:
                                    print(f"  {key.capitalize()}: OUD: {old[key]} → NIEUW: {new[key]}")

                    # 5b) Nieuwe listings toegevoegd (als lijst langer is)
                    if len(new_listings) > len(previous_listings):
                        for added in new_listings[min_len:]:
                            print("\nNieuwe listing toegevoegd:")
                            for key, value in added.items():
                                print(f"  {key.capitalize()}: {value}")

                    # 5c) Listings verwijderd (als lijst korter is)
                    if len(new_listings) < len(previous_listings):
                        for removed in previous_listings[min_len:]:
                            print("\nListing verwijderd:")
                            for key, value in removed.items():
                                print(f"  {key.capitalize()}: {value}")

                    # 5d) Sla nieuwe data op voor volgende iteratie
                    previous_listings = new_listings
                    pause()

                else:
                    # Geen wijzigingen: aftellen en opnieuw checken
                    for i in range(checker_delay):
                        if i == 1:
                            print(f"Checking...")
                        else:
                            print(f"Geen wijzigingen gevonden, opnieuw controleren over {checker_delay - i} seconden...",end="\r",)
                            time.sleep(1)

        # Gebruiker kan met Ctrl+C stoppen
        except KeyboardInterrupt:
            print("\nUser stopped the program.")
            exit()

        # Foutafhandeling bij onverwachte issues
        except Exception as e:
            print(f"Root Error: {e}")

        finally:
            driver.quit()

clear() # cleans console at start of program

if __name__ == "__main__":
    main()
