#!/bin/bash

echo "Installing dependencies..."
apt-get update && apt-get install -y wget curl unzip gnupg

# Download a pre-built portable version of Chromium
echo "Downloading Chromium..."
mkdir -p /opt/chromium
wget -qO /opt/chromium/chrome.zip "https://download-chromium.appspot.com/dl/Linux_x64"

# Unzip the downloaded file
echo "Extracting Chromium..."
unzip /opt/chromium/chrome.zip -d /opt/chromium/
rm /opt/chromium/chrome.zip

# Find the Chromium binary
CHROME_PATH=$(find /opt/chromium/ -type f -name "chrome" | head -n 1)

if [ -z "$CHROME_PATH" ]; then
    echo "Error: Chromium not found after manual download!"
    exit 1
fi

# Set environment variables to use the downloaded Chromium binary
export GOOGLE_CHROME_BIN="$CHROME_PATH"
export CHROMIUM_PATH="$CHROME_PATH"

echo "Chromium installed at $GOOGLE_CHROME_BIN"

# Start FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000
