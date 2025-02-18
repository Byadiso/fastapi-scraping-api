import os
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ CORS fix
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

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://fastapi-scraping-api-production.up.railway.app"],  # Update with frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Get Chromium binary path from environment variable (for Render deployment)
chromium_path = os.getenv("GOOGLE_CHROME_BIN")

# Fallback for local environments if GOOGLE_CHROME_BIN is not set
if not chromium_path:
    if os.name == "nt":  # Windows
        chromium_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    else:  # Linux/macOS
        chromium_path = "/usr/bin/google-chrome"

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
chrome_options.binary_location = chromium_path  # Set Chromium binary location

# Function to get a Selenium WebDriver


def get_driver():
    chrome_driver_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_driver_path)
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

# Scrape Matches


def scrape_matches():
    try:
        driver = get_driver()
        url = "https://superbet.pl/zaklady-bukmacherskie/pilka-nozna/dzisiaj"
        driver.get(url)

        # Wait until event cards are available
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-card"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        matches = []
        for match_element in soup.find_all("div", class_="event-card"):
            home_team = match_element.find(
                "div", class_="e2e-event-team1-name")
            away_team = match_element.find(
                "div", class_="e2e-event-team2-name")
            match_time = match_element.find("span", class_="event-card-label")

            if home_team and away_team and match_time:
                match = {
                    "homeTeam": home_team.get_text(strip=True),
                    "awayTeam": away_team.get_text(strip=True),
                    "time": match_time.get_text(strip=True),
                    "odds": {"homeWin": "N/A", "draw": "N/A", "awayWin": "N/A"},
                }

                # Extract odds
                odds = match_element.select(
                    "div.odd-offer div:nth-child(1) button div span.odd-button__odd-value-new")
                if len(odds) >= 3:
                    match["odds"]["homeWin"] = odds[0].get_text(
                        strip=True).replace(",", "")
                    match["odds"]["draw"] = odds[1].get_text(
                        strip=True).replace(",", "")
                    match["odds"]["awayWin"] = odds[2].get_text(
                        strip=True).replace(",", "")

                matches.append(match)

        return matches

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return []

# scrape yesterday match to check results


def scrape_matches_yesterday():
    try:
        driver = get_driver()
        url = "https://superbet.pl/zaklady-bukmacherskie/pilka-nozna/2025-02-17"
        driver.get(url)

        # Wait until event cards are available
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-card"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        matches = []
        for match_element in soup.find_all("div", class_="event-card"):
            home_team = match_element.find(
                "div", class_="e2e-event-team1-name")
            away_team = match_element.find(
                "div", class_="e2e-event-team2-name")
            match_time = match_element.find("span", class_="event-card-label")

            if home_team and away_team and match_time:
                match = {
                    "homeTeam": home_team.get_text(strip=True),
                    "awayTeam": away_team.get_text(strip=True),
                    "time": match_time.get_text(strip=True),
                    "odds": {"homeWin": "N/A", "draw": "N/A", "awayWin": "N/A"},
                }

                # Extract odds
                odds = match_element.select(
                    "div.odd-offer div:nth-child(1) button div span.odd-button__odd-value-new")
                if len(odds) >= 3:
                    match["odds"]["homeWin"] = odds[0].get_text(
                        strip=True).replace(",", "")
                    match["odds"]["draw"] = odds[1].get_text(
                        strip=True).replace(",", "")
                    match["odds"]["awayWin"] = odds[2].get_text(
                        strip=True).replace(",", "")

                matches.append(match)

        return matches

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return []


# API Endpoint: Get all matches
@app.get("/matches")
def get_all_matches():
    matches = scrape_matches()
    return {"matches": matches}

# API Endpoint: Get matches with low odds (home win < 1.50)


@app.get("/low-odds-matches")
def get_low_odds_matches():
    matches = scrape_matches()
    low_odds_matches = [match for match in matches if match["odds"]
                        ["homeWin"] != "N/A" and float(match["odds"]["homeWin"]) < 1.50]
    return {"lowOddsMatches": low_odds_matches}


# API Endpoint: Get yesterday's matches with low odds result(home win < 1.50)
@app.get("/yesterday-matches")
def get_yesterday_results():
    matches = scrape_matches_yesterday()
    return {"yesterdayMatches": matches}


# Cleanup Selenium driver when FastAPI shuts down
atexit.register(lambda: print("Server shutting down. Cleanup complete."))

# Run the server:
# uvicorn api:app --host 0.0.0.0 --port 10000 --reload
