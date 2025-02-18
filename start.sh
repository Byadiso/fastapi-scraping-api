#!/bin/bash

echo "Installing dependencies..."

# Only install on Render (use environment variable check)
if [ "$RENDER" == "true" ]; then
  echo "Installing Chromium on Render..."

  # Install dependencies for Chromium
  apt-get update && apt-get install -y wget curl unzip gnupg

  # Download and extract Chromium (Render setup)
  mkdir -p ./chromium
  wget -qO ./chromium/chrome.zip "https://download-chromium.appspot.com/dl/Linux_x64"
  unzip ./chromium/chrome.zip -d ./chromium/
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

  # Get Chromium version
  CHROMIUM_VERSION=$(./chromium/chrome-linux/chrome --version 2>&1 | awk '{print $3}' | cut -d'.' -f1,2)
  echo "Chromium version detected: $CHROMIUM_VERSION"

  # Download the matching ChromeDriver version for Chromium
  # Note: We'll now directly match the version based on Chromium version
  case "$CHROMIUM_VERSION" in
    "135.0")
      CHROMEDRIVER_VERSION="135.0.7022.0"
      ;;
    *)
      echo "Error: No matching ChromeDriver version for Chromium version $CHROMIUM_VERSION!"
      exit 1
      ;;
  esac

  # Download the correct ChromeDriver for the Chromium version
  echo "Downloading ChromeDriver version $CHROMEDRIVER_VERSION..."
  wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" -O chromedriver.zip

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
