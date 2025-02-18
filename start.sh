#!/bin/bash

echo "Installing dependencies..."
apt-get update && apt-get install -y wget curl unzip gnupg

# Download a pre-built portable version of Chromium to a writable directory
echo "Downloading Chromium..."
mkdir -p ./chromium
wget -qO ./chromium/chrome.zip "https://download-chromium.appspot.com/dl/Linux_x64"

# Unzip the downloaded file
echo "Extracting Chromium..."
unzip ./chromium/chrome.zip -d ./chromium/
rm ./chromium/chrome.zip

# Log the directory structure to see where the binaries are
echo "Listing contents of ./chromium:"
ls -l ./chromium/

# Search for the chromium binary
CHROME_PATH=$(find ./chromium/ -type f -name "chrome" | head -n 1)

# Log if binary is found or not
if [ -z "$CHROME_PATH" ]; then
    echo "Error: Chromium not found after manual download!"
    exit 1
else
    echo "Chromium found at $CHROME_PATH"
fi

# Set environment variables for Chromium
export GOOGLE_CHROME_BIN="$CHROME_PATH"
export CHROMIUM_PATH="$CHROME_PATH"

echo "Chromium installed at $GOOGLE_CHROME_BIN"

# Start FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000
