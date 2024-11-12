#!/bin/bash
# Install dependencies for the C agent

# Check if libcurl is installed, if not, install it
if ! ldconfig -p | grep -q libcurl; then
    echo "libcurl not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y libcurl4-openssl-dev
else
    echo "libcurl is already installed."
fi

# Compile the C agent
make
