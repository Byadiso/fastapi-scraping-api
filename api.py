from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from bs4 import BeautifulSoup  # Make sure BeautifulSoup is imported

app = FastAPI()

# Setup Selenium WebDriver
chrome_options = Options()

# Check if we are in a cloud environment (e.g. Render) and use the Chromium path if it exists.
if os.getenv('RENDER_ENV', 'false') == 'true':
    chrome_options.binary_location = '/usr/bin/chromium'  # Path to Chromium in Render
else:
    chrome_options.add_argument("--no-sandbox")  # Additional flags for local usage
    chrome_options.add_argument("--disable-dev-shm-usage")

chrome_options.add_argument("--headless")  # Run in headless mode

# Use the ChromeDriverManager to install the correct chromedriver version.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to scrape match data
def scrape_matches():
    url = "https://superbet.pl/zaklady-bukmacherskie/pilka-nozna/dzisiaj"
    driver.get(url)
    driver.implicitly_wait(5)

    # Scroll to load full content
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    while scroll_attempts < 10:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
        else:
            scroll_attempts = 0
        last_height = new_height

    # Scrape the data
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    matches = []

    for match_element in soup.find_all("div", class_="event-card"):
        match = {
            "homeTeam": match_element.find("div", class_="e2e-event-team1-name").get_text(strip=True) if match_element.find("div", class_="e2e-event-team1-name") else "N/A",
            "awayTeam": match_element.find("div", class_="e2e-event-team2-name").get_text(strip=True) if match_element.find("div", class_="e2e-event-team2-name") else "N/A",
            "time": match_element.find("span", class_="event-card-label").get_text(strip=True) if match_element.find("span", class_="event-card-label") else "N/A",
            "odds": {"homeWin": "N/A", "draw": "N/A", "awayWin": "N/A"}
        }

        odds = match_element.select("div.odd-offer div:nth-child(1) button div span.odd-button__odd-value-new")
        if len(odds) >= 3:
            match["odds"]["homeWin"] = odds[0].get_text(strip=True).replace(',', '')
            match["odds"]["draw"] = odds[1].get_text(strip=True).replace(',', '')
            match["odds"]["awayWin"] = odds[2].get_text(strip=True).replace(',', '')

        matches.append(match)

    return matches

@app.get("/matches")
def get_all_matches():
    matches = scrape_matches()
    return {"matches": matches}

@app.get("/low-odds-matches")
def get_low_odds_matches():
    matches = scrape_matches()
    low_odds_matches = [match for match in matches if match["odds"]["homeWin"] != "N/A" and float(match["odds"]["homeWin"]) < 1.50]
    return {"lowOddsMatches": low_odds_matches}
