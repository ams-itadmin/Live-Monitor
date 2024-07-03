#!/bin/bash

# Update and install necessary packages
sudo apt update
sudo apt install -y git wireshark bridge-utils net-tools python3-pip python3-venv -y

# Create a venv
python3 -m venv venv 

source venv/bin/activate

# Install required Python packages
pip3 install -r requirements.txt

# Create an empty configuration file
touch config.json

echo "Installation complete. You can now run the setup script."
