FROM n8nio/n8n:latest

USER root

# Install Python, pip, and required libraries
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    py3-setuptools

# Install Python packages with break-system-packages flag
RUN pip3 install --break-system-packages requests beautifulsoup4

RUN mkdir -p /data/scripts

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

USER node
