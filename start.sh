#!/bin/bash

echo "Installing dependencies..."

# Only install on Render (use environment variable check)
if [ "$RENDER" == "true" ]; then
  echo "Installing Chromium on Render..."

  # Install dependencies for Chromium
  apt-get update && apt-get install -y wget curl unzip gnupg

  # Download and extract Chromium (Force version 114 for compatibility)
  mkdir -p ./chromium
  wget -qO ./chromium/chrome.zip "https://download-chromium.appspot.com/dl/Linux_x64?type=tar"
  tar -xvzf ./chromium/chrome.zip -C ./chromium/
  rm ./chromium/chrome.zip

  # Log the directory structure to see where the binaries are
  echo "Listing contents of ./chromium:"
  ls -l ./chromium/

  # Find the Chromium binary
  CHROME_PATH=$(find ./chromium/ -type f -name "chrome" | head -n 1)

  # Log and set the binary
  if [ -z "$CHROME_PATH" ]; then
    echo "Error: Chromium not found after manual download!"
    exit 1
  else
    echo "Chromium found at $CHROME_PATH"
    export GOOGLE_CHROME_BIN="$CHROME_PATH"
    export CHROMIUM_PATH="$CHROME_PATH"
  fi

  # Ensure matching ChromeDriver version 114.0.5735.90
  CHROMIUM_VERSION="114.0.5735.90"  # Explicit version for Chromium 114
  echo "Chromium version forced to $CHROMIUM_VERSION"

  # Download ChromeDriver for version 114
  echo "Downloading ChromeDriver for Chromium version 114..."
  wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" -O chromedriver.zip

  # Unzip and move ChromeDriver to the proper location
  unzip chromedriver.zip
  mv chromedriver /usr/local/bin/chromedriver
  rm chromedriver.zip

  echo "ChromeDriver installed at /usr/local/bin/chromedriver"
else
  # Handle local environment (do nothing related to Chromium installation)
  echo "Running locally - skipping Chromium installation"
fi

# Start FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000
