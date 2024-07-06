#!/bin/bash

# Update and install necessary packages
sudo apt update
sudo apt install -y bridge-utils net-tools python3-pip python3-venv -y
# sudo apt install wireshark -y

# Create a venv
python3 -m venv venv 

# Activate venv
source venv/bin/activate

# Install required Python packages
pip3 install -r requirements.txt

# Create an empty configuration file
touch config.json

# Create an empty log file
touch general.log

echo "Installation complete. You can now run the setup script."
echo "To activate vitrual environment:  source venv/bin/activate"
