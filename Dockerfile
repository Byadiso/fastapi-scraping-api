# Start from the official Python image
FROM python:3.9-slim

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set the environment variable for Render (optional)
ENV RENDER_ENV=true

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app with uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
