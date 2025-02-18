import os
import subprocess
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import atexit

app = FastAPI()

# Get Chromium binary path from environment variable (set by your shell script on Render)
chromium_path = os.getenv("GOOGLE_CHROME_BIN")

# Fallback for local environment if GOOGLE_CHROME_BIN is not set
if not chromium_path:
    # Set default path for local environments (adjust if necessary)
    if os.name == "nt":  # Windows
        chromium_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    else:  # Linux/macOS
        chromium_path = "/usr/bin/google-chrome"  # or the path where Chrome is installed

if not os.path.exists(chromium_path):
    print(f"Error: Google Chrome binary not found at {chromium_path}")
    exit(1)

print(f"Google Chrome path: {chromium_path}")

# Initialize Chrome Options
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# Set the correct Chromium binary location
chrome_options.binary_location = chromium_path

# Create a Selenium WebDriver instance using webdriver-manager to automatically handle ChromeDriver version
def get_driver():
    # This will automatically download and setup the correct version of ChromeDriver
    chrome_driver_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_driver_path)
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

# Scrape Matches
def scrape_matches():
    try:
        driver = get_driver()
        url = "https://superbet.pl/zaklady-bukmacherskie/pilka-nozna/dzisiaj"
        driver.get(url)

        # Wait until the elements are available on the page (change this condition as per your requirement)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-card"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        matches = []
        for match_element in soup.find_all("div", class_="event-card"):
            home_team = match_element.find("div", class_="e2e-event-team1-name")
            away_team = match_element.find("div", class_="e2e-event-team2-name")
            match_time = match_element.find("span", class_="event-card-label")
            
            if home_team and away_team and match_time:
                match = {
                    "homeTeam": home_team.get_text(strip=True),
                    "awayTeam": away_team.get_text(strip=True),
                    "time": match_time.get_text(strip=True),
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
