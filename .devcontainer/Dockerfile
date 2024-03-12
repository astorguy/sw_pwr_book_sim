FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

WORKDIR /app

COPY bookworm-backports.list /etc/apt/sources.list.d/

# Install ngspice and kicad
RUN apt-get update && \
    apt-get -y install ngspice && \
    apt-get -t bookworm-backports -y install kicad && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt
