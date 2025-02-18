#!/bin/bash

# Install dependencies
echo "Installing dependencies for Google Chrome..."

# Install required system packages
apt-get update
apt-get install -y wget curl unzip gnupg

# Install dependencies for Chrome
apt-get install -y \
    libxss1 \
    libappindicator3-1 \
    libindicator3-0.7 \
    libdbusmenu-glib4 \
    libgdk-pixbuf2.0-0 \
    libnss3 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    xdg-utils \
    libgbm-dev

# Download and install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -f -y
rm google-chrome-stable_current_amd64.deb

# Set environment variables for the Chrome binary location
export GOOGLE_CHROME_BIN=/usr/bin/google-chrome
export CHROMIUM_PATH=/usr/bin/google-chrome

echo "Starting FastAPI app..."
# Start your FastAPI app
# uvicorn api:app --host 0.0.0.0 --port 8000
uvicorn api:app --host 0.0.0.0 --port 10000
