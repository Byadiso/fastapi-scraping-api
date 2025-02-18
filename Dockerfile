# Use an official Python runtime as the base image
FROM python:3.9-buster

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system utilities and some essential packages
RUN apt-get update && apt-get install -y apt-utils curl gnupg wget && \
    apt-get install -y libxss1 libappindicator3-1 libdbusmenu-glib4 \
    libgdk-pixbuf2.0-0 libnss3 libxtst6 libatk1.0-0 libatk-bridge2.0-0 \
    libx11-xcb1 xdg-utils libgbm-dev ca-certificates && \
    apt-get upgrade -y

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || (apt-get install -f -y && dpkg -i google-chrome-stable_current_amd64.deb) && \
    rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin && \
    rm chromedriver_linux64.zip

# Clean up and finalize the setup
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for the Chrome binary and ChromeDriver path
ENV GOOGLE_CHROME_BIN=/usr/bin/google-chrome
ENV CHROMIUM_PATH=/usr/bin/google-chrome
ENV PATH=$PATH:/usr/local/bin

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . /app/

# Expose port 8000 for FastAPI
EXPOSE 8000

# Set the command to run the FastAPI app using uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
