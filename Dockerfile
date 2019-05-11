FROM ubuntu:disco

RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install selenium
