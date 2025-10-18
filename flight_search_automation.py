# flight_search_automation.py

from playwright.sync_api import sync_playwright
from datetime import datetime,timedelta
import json

def search_flights(origin="Bangalore", destination="Delhi", journey_date=None):
    if journey_date is None:
        # Default: tomorrow's date
        journey_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True to run without browser UI
        page = browser.new_page()
        
        # Open budgetticket flight search page
        page.goto("https://www.budgetticket.in/flights")

        # Fill origin city
        page.fill("input[placeholder='From']", origin)
        page.wait_for_timeout(1000)  # small delay to ensure auto-suggestion appears
        page.keyboard.press("Enter")

        # Fill destination city
        page.fill("input[placeholder='To']", destination)
        page.wait_for_timeout(1000)
        page.keyboard.press("Enter")

        # Fill journey date
        page.fill("input[name='departDate']", journey_date)
        page.wait_for_timeout(500)

        # Click Search button
        page.click("button[type='submit']")

        # Wait until flight results load
        page.wait_for_selector(".flights__list-item", timeout=60000)

        # Extract flight details
        flight_cards = page.query_selector_all(".flights__list-item")
        search_datetime = datetime.utcnow().isoformat() + "Z"

        for card in flight_cards:
            try:
                airline = card.query_selector(".airline-name").inner_text().strip()
                flight_number = card.query_selector(".flight-number").inner_text().strip()
                departure = card.query_selector(".depart-time").inner_text().strip()
                arrival = card.query_selector(".arrival-time").inner_text().strip()
                price = card.query_selector(".fare-amount").inner_text().strip()

                results.append({
                    "airline": airline,
                    "flight_number": flight_number,
                    "departure": departure,
                    "arrival": arrival,
                    "price": price,
                    "origin": origin,
                    "destination": destination,
                    "searchdatetime": search_datetime
                })
            except Exception as e:
                continue  # skip cards with missing info

        browser.close()

    # Save results to JSON file
    with open("flight_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"Total Flights Extracted: {len(results)}")
    return results


# Test the function
if __name__ == "__main__":
    search_flights()
