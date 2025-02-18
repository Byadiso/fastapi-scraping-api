from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

chromedriver_path = r"C:\path\to\chromedriver.exe"  # Adjust the path to chromedriver.exe
chrome_service = Service(chromedriver_path)

try:
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get('http://www.google.com/')

    # Let's print the title of the webpage
    print(driver.title)

    driver.quit()
except Exception as e:
    print(f"Error: {e}")
