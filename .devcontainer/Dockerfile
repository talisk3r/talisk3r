FROM python:3.11-slim

# Install Git and cleanup apt cache
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and switch to it
RUN useradd -m vscode && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Copy bashrc with correct ownership
COPY --chown=vscode:vscode .devcontainer/.bashrc /home/vscode/.bashrc

# Set working directory and permissions (convention for DevContainers)
WORKDIR /workspace

# Copy requirements.txt from PROJECT ROOT to /workspace
COPY requirements.txt .
# COPY --chown=vscode:vscode requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Copy all project files (except what's in .dockerignore)
COPY --chown=vscode:vscode . .

COPY --chown=vscode:vscode .devcontainer/.bashrc /home/vscode/.bashrc

USER vscode

