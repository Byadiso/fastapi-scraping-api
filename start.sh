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
uvicorn api:app --host 0.0.0.0 --port 10000#!/bin/bash

echo "Installing Chromium manually..."

# Update package list
apt-get update

# Install required dependencies
apt-get install -y wget curl unzip gnupg software-properties-common

# Download Chromium directly
mkdir -p /opt/chromium
wget -qO- https://download-chromium.appspot.com/dl/Linux_x64 | tar xJ -C /opt/chromium

# Set environment variables for Chromium
export GOOGLE_CHROME_BIN="/opt/chromium/chrome"
export CHROMIUM_PATH="/opt/chromium/chrome"

echo "Chromium installed at $GOOGLE_CHROME_BIN"

# Start FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000

