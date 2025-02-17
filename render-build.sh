#!/usr/bin/env bash

# Install Chromium
apt-get update
apt-get install -y chromium-browser

# Ensure correct permissions
chmod +x /usr/bin/chromium-browser
