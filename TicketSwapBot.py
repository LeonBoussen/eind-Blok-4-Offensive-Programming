from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Back, Style, init
from time import sleep as delay
from datetime import datetime as time
from os import system as cmd
import random


#variables
proxyList = []
proxyForGet = ""

#console colors
cGreen = Fore.GREEN
cRed = Fore.RED
cMagenta = Fore.MAGENTA
cBlue = Fore.BLUE

#random UA list
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/100.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36 OPR/100.0.0.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G970U) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/100.0.0.0 Mobile Safari/537.36",
]

def start():
    #Setup
    cmd("title TicketSwapBot v1")
    cmd("cls")
    print(cMagenta + "Welcome to TicketSniper v1\n\n\n")
    link = input("Enter Event Link: ")
    proxyPath = input("Enter proxy file: ")
    timeout_seconds = int(input("Timeout: "))
    cmd("cls")

    #Read Proxy file and adds to array
    with open(f'{proxyPath}', 'r') as proxyFile:
        for proxy in proxyFile:
            proxyList.append(proxy.strip())
    
    return link

#Functions
#Error handling + Error to log in local dir
def errorLog(error):
    with open("Error Log.txt", 'a') as file:
        file.write(str(error) + '\n\n\n')

#program main
def checkTicket(link):
    #global variables
    global proxyForGet
    #Scope variables
    ticketlinks = []
    proxyForGet = random.choice(proxyList)

    #Setup - browser/antibot
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server=%s" % proxyForGet) #Add the proxy as argument 
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") #Adding argument to disable the AutomationControlled flag 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) #Exclude the collection of enable-automation switches 
    chrome_options.add_experimental_option("useAutomationExtension", False) #Turn-off userAutomationExtension
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=chrome_options)#Add set options to Chrome
    random_UA = random.choice(user_agents) #Getting Random UA
    browser.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": random_UA}) #Using choisen UA
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") #Changing the property of the navigator value for webdriver to undefined 
    browser.get(link)


    #initial info
    cmd("cls")
    print(cBlue + "Browser setup complete")
    print(cBlue + f"using proxy: {proxyForGet} with User-Agent: {random_UA}")


    tickets = browser.find_elements(By.CSS_SELECTOR, 'a[data-testid="listing"]')
    if tickets:
        print(cGreen + "Tickets found!")
        for ticket in tickets:
            ticketlinks.append(ticket.get_attribute("href"))
        print(cBlue + f"Found {len(ticketlinks)} tickets")
        print(cBlue + "prining tickets...")
        for ticket in ticketlinks:
            print(cGreen + f"Ticket link: {ticket}")
        
url = start()

def search():
    while True:
        try:
            while len(proxyList) > 1:
                checkTicket(url)
            else:
                print("No proxies left for anti bot")
        except ConnectionError as e:
            proxyList.remove(proxyForGet)
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            errorLog(f"Error occured at {time.now()}!\nError info:\nProxy: {proxyForGet}\n{e}\n\n--------------------------------")
        finally:
            print(Fore.YELLOW + "Loop done!")

