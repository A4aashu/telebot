FROM python:3.13-slim

# Install system packages needed for pyzbar and OpenCV
RUN apt-get update && \
    apt-get install -y libzbar0 build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /opt/app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start your bot
CMD [ "python", "bot.py" ]
