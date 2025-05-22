import requests
import yfinance as yf
import asyncio

import keyboard # for testing
import time # for testing


# Global variables
simulated_mode = False

def search_ticker(name: str) -> str:
    url = "https://autoc.finance.yahoo.com/autoc"
    params = {"query": name, "region": 1, "lang": "en"}
    response = requests.get(url, params=params)
    data = response.json()
    results = data.get("ResultSet", {}).get("Result", [])
    if not results:
        raise ValueError(f"No ticker found for '{name}'.")
    return results[0]["symbol"]

def get_price(ticker: str) -> float:
    ticker_obj = yf.Ticker(ticker)
    data = ticker_obj.info
    price = data.get('regularMarketPrice')
    if price is None:
        raise ValueError(f"Could not fetch price for ticker '{ticker}'.")
    return price

def test_price(price: float) -> float:
    if keyboard.is_pressed('up'):
        time.sleep(0.1)  # Small delay to avoid rapid key presses
        return price + 1.0
    if keyboard.is_pressed('down'):
        time.sleep(0.1)  # Small delay to avoid rapid key presses
        return price - 1.0
    else:
        return price

def checker_logic(alert: float, price: float, symbol: str):
    global simulated_mode
    # if checking if price is above current price and then alert if target is reached or if it is more than the target
    if alert > price:
        while True:
            if not simulated_mode:
                current_price = get_price(symbol)

                # Simulate price change for testing
                sim = test_price(current_price)
                if sim != current_price:
                    current_price = sim
                    simulated_mode = True

                if current_price >= alert:
                    print(f"Alert! {symbol} has reached your target price of ${alert:.2f}. Current price: ${current_price:.2f}")
                    break
                else:
                    print(f"{symbol} is currently at ${current_price:.2f}. Waiting for target to be hit ${alert}...")

            elif simulated_mode:
                sim = test_price(current_price)
                if sim != current_price:
                    current_price = sim

                if current_price >= alert:
                    print(f"Alert! {symbol} has reached your target price of ${alert:.2f}. Current price: ${current_price:.2f}")
                    break
                else:
                    print(f"{symbol} is currently at ${current_price:.2f}. Waiting for target to be hit ${alert}...")


    # if checking if price is below current price and then alert if target is reached or if it is less than the target
    if alert < price:
        while True:
            current_price = get_price(symbol)
            if current_price <= alert:
                print(f"Alert! {symbol} has dropped below your target price of ${alert:.2f}. Current price: ${current_price:.2f}")
                break
            else:
                print(f"{symbol} is currently at ${current_price:.2f}. Waiting for target to be hit ${alert}...")

    # if user target is the same as the current price
    if alert == price:
        print(f"Alert! {symbol} is already your target price of ${alert:.2f}. Current price: ${price:.2f}")

def main():
    while True:
        user_input = input("Enter stock tickers or company names (comma-separated): ")
        entries = [e.strip() for e in user_input.split(',') if e.strip()]

        if not entries:
            print("No entries provided.")
            

        print("\nProcessing entries...\n")
        for entry in entries:
            symbol = entry.upper()
            try:
                if ((not symbol.isalpha() and not symbol.startswith('^'))) or len(symbol) > 5:
                    print(f"Looking up ticker for '{entry}'...")
                    symbol = search_ticker(entry)
                    print(f"Found symbol: {symbol}")

                price = get_price(symbol)
                print(f"{symbol}: ${price:.2f}")

                alert = float(input(f"Set alert for {symbol} at price: $"))
                checker_logic(alert, price, symbol)

            except Exception as e:
                print(f"Error for '{entry}': {e}")
