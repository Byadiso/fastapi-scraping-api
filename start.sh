#!/bin/bash

# Install dependencies
echo "Installing dependencies for Google Chrome..."

# Install required system packages (without sudo)
apt-get update && apt-get install -y wget curl unzip gnupg

# Download the latest Chrome binary
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > chrome.deb

# Extract the Chrome package manually (no root)
mkdir -p /opt/chrome
dpkg-deb -x chrome.deb /opt/chrome/
rm chrome.deb

# Set environment variables to use the extracted Chrome
export GOOGLE_CHROME_BIN="/opt/chrome/opt/google/chrome/google-chrome"
export CHROMIUM_PATH="/opt/chrome/opt/google/chrome/google-chrome"

echo "Google Chrome installed successfully at $GOOGLE_CHROME_BIN"

# Start your FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000
