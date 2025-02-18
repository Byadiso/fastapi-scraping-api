#!/bin/bash

echo "Updating package list..."
apt-get update

echo "Installing Chromium..."
apt-get install -y chromium-browser

echo "Checking Chromium installation..."
which chromium-browser || which chromium || which google-chrome

# Find Chromium binary manually
if [ -f "/usr/bin/chromium-browser" ]; then
    export GOOGLE_CHROME_BIN="/usr/bin/chromium-browser"
elif [ -f "/usr/bin/chromium" ]; then
    export GOOGLE_CHROME_BIN="/usr/bin/chromium"
elif [ -f "/usr/bin/google-chrome" ]; then
    export GOOGLE_CHROME_BIN="/usr/bin/google-chrome"
else
    echo "Error: Chromium not found after installation!"
    exit 1
fi

export CHROMIUM_PATH="$GOOGLE_CHROME_BIN"

echo "Chromium installed at $GOOGLE_CHROME_BIN"

# Start FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000
