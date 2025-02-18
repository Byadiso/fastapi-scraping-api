#!/bin/bash

echo "Installing Chromium..."

# Update package list and install Chromium
apt-get update && apt-get install -y chromium-browser

# Set environment variables to use Chromium
export GOOGLE_CHROME_BIN="/usr/bin/chromium-browser"
export CHROMIUM_PATH="/usr/bin/chromium-browser"

echo "Chromium installed at $GOOGLE_CHROME_BIN"

# Start FastAPI app
uvicorn api:app --host 0.0.0.0 --port 10000
