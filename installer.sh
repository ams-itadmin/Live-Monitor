#!/bin/bash

# Update and install necessary packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y git wireshark bridge-utils net-tools python3-pip -y

# Install required Python packages
pip3 install -r requirements.txt

# Create an empty configuration file
touch config.json

echo "Installation complete. You can now run the setup script."
