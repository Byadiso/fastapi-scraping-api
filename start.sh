#!/bin/bash

echo "Installing Google Chrome (non-root)..."

# Install required system packages
apt-get update && apt-get install -y wget curl unzip gnupg

# Download the latest Chrome binary
wget -qO chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Extract the Chrome package manually (since we don't have root access)
mkdir -p /opt/chrome
dpkg-deb -x chrome.deb /opt/chrome/
rm chrome.deb

# Set environment variables to use the extracted Chrome
export GOOGLE_CHROME_BIN="/opt/chrome/opt/google/chrome/google-chrome"
export CHROMIUM_PATH="/opt/chrome/opt/google/chrome/google-chrome"

echo "Google Chrome installed at $GOOGLE_CHROME_BIN"

# Start FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000
