import os
import subprocess
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import atexit

app = FastAPI()

# Detect Chromium and ChromeDriver paths
chromium_path = subprocess.getoutput("which google-chrome") or subprocess.getoutput("which chromium")
chromedriver_path = subprocess.getoutput("which chromedriver")

print(f"Google Chrome path: {chromium_path}")
print(f"ChromeDriver path: {chromedriver_path}")

# Initialize Chrome Options
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# Set the correct Chromium binary location
chrome_options.binary_location = chromium_path

# Create a Selenium WebDriver instance
def get_driver():
    chrome_service = Service(chromedriver_path)
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

# Scrape Matches
def scrape_matches():
    try:
        driver = get_driver()
        url = "https://superbet.pl/zaklady-bukmacherskie/pilka-nozna/dzisiaj"
        driver.get(url)
        driver.implicitly_wait(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        matches = []
        for match_element in soup.find_all("div", class_="event-card"):
            match = {
                "homeTeam": match_element.find("div", class_="e2e-event-team1-name").get_text(strip=True) if match_element.find("div", class_="e2e-event-team1-name") else "N/A",
                "awayTeam": match_element.find("div", class_="e2e-event-team2-name").get_text(strip=True) if match_element.find("div", class_="e2e-event-team2-name") else "N/A",
                "time": match_element.find("span", class_="event-card-label").get_text(strip=True) if match_element.find("span", class_="event-card-label") else "N/A",
                "odds": {"homeWin": "N/A", "draw": "N/A", "awayWin": "N/A"},
            }

            # Extract odds
            odds = match_element.select("div.odd-offer div:nth-child(1) button div span.odd-button__odd-value-new")
            if len(odds) >= 3:
                match["odds"]["homeWin"] = odds[0].get_text(strip=True).replace(",", "")
                match["odds"]["draw"] = odds[1].get_text(strip=True).replace(",", "")
                match["odds"]["awayWin"] = odds[2].get_text(strip=True).replace(",", "")

            matches.append(match)

        return matches

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return []

@app.get("/matches")
def get_all_matches():
    matches = scrape_matches()
    return {"matches": matches}

@app.get("/low-odds-matches")
def get_low_odds_matches():
    matches = scrape_matches()
    low_odds_matches = [match for match in matches if match["odds"]["homeWin"] != "N/A" and float(match["odds"]["homeWin"]) < 1.50]
    return {"lowOddsMatches": low_odds_matches}

# Cleanup Selenium driver when FastAPI shuts down
atexit.register(lambda: print("Server shutting down. Cleanup complete."))
