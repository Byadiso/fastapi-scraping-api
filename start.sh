#!/bin/bash

echo "Installing Chromium..."

# Update package list and install Chromium
apt-get update && apt-get install -y chromium-browser

# Find the actual Chromium binary path
CHROME_PATH=$(which chromium-browser || which chromium)

if [ -z "$CHROME_PATH" ]; then
    echo "Error: Chromium not found!"
    exit 1
fi

# Set environment variables for Chromium
export GOOGLE_CHROME_BIN="$CHROME_PATH"
export CHROMIUM_PATH="$CHROME_PATH"

echo "Chromium installed at $GOOGLE_CHROME_BIN"

# Start FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000
