import psutil
import json
import socket
import subprocess
import os
import logging
from datetime import datetime

# Setup Config File
config_file = 'config.json'

# Default Config
default_config = {
    'interfaces': ["", ""],
    'bridge': ""
}

# Configure logging
logging.basicConfig(
    filename='general.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_event(event):
    logging.info(event)

def list_interfaces():
    interfaces = psutil.net_if_addrs()
    return [iface for iface in interfaces if iface != 'lo']

def parse_network_info():
    interfaces = psutil.net_if_addrs()
    parsed_info = {}

    for iface, addrs in interfaces.items():
        iface_info = {
            'MAC': None,
            'IPv4': None,
        }
        for addr in addrs:
            if addr.family == socket.AF_PACKET:
                iface_info['MAC'] = addr.address
            elif addr.family == socket.AF_INET:
                iface_info['IPv4'] = {
                    'address': addr.address,
                    'netmask': addr.netmask
                }
        parsed_info[iface] = iface_info

    return parsed_info

def print_network_info(parsed_info):
    for iface, info in parsed_info.items():
        print(f"Interface: {iface}")
        print(f"  MAC Address: {info['MAC']}")
        if info['IPv4']:
            print(f"  IPv4 Address: {info['IPv4']['address']}")
            print(f"  IPv4 Netmask: {info['IPv4']['netmask']}")
        print("-" * 40)

def show_bridge_info():
    # Use subprocess to call brctl show
    result = subprocess.run(['brctl', 'show'], stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))

    # Use psutil to display network interface details
    parsed_info = parse_network_info()
    print_network_info(parsed_info)

def create_initial_config(default_config):
    with open(config_file, 'w') as f:
        json.dump(default_config, f, indent=4)

def write_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def read_config():
    if not os.path.exists(config_file):
        # Create the config file with default values if it doesn't exist
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    else:
        # Read the existing config file
        with open(config_file, 'r') as f:
            return json.load(f)

def create_bridge(interface1, interface2):
    subprocess.run(['sudo', 'ip', 'link', 'add', 'name', 'br0', 'type', 'bridge'])
    subprocess.run(['sudo', 'ip', 'link', 'set', interface1, 'master', 'br0'])
    subprocess.run(['sudo', 'ip', 'link', 'set', interface2, 'master', 'br0'])
    subprocess.run(['sudo', 'ip', 'link', 'set', 'br0', 'up'])
    subprocess.run(['sudo', 'ip', 'link', 'set', interface1, 'promisc', 'on'])
    subprocess.run(['sudo', 'ip', 'link', 'set', interface2, 'promisc', 'on'])

    config = {
        'interfaces': [interface1, interface2],
        'bridge': 'br0'
    }
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

    log_event(f"Bridge created: interfaces {interface1} and {interface2}, bridge br0")
    
def remove_bridge():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        interface1, interface2 = config['interfaces']
        bridge = config['bridge']

        if not interface1 or not interface2 or not bridge:
            print("Configuration file has empty fields. Please create a bridge first.")
            return

        subprocess.run(['sudo', 'ip', 'link', 'set', interface1, 'promisc', 'off'])
        subprocess.run(['sudo', 'ip', 'link', 'set', interface2, 'promisc', 'off'])
        subprocess.run(['sudo', 'ip', 'link', 'set', bridge, 'down'])
        subprocess.run(['sudo', 'ip', 'link', 'delete', bridge, 'type', 'bridge'])

        log_event(f"Bridge removed: {bridge}, interfaces {interface1} and {interface2}")

        print(f"Bridge {bridge} and promiscuous mode on {interface1} and {interface2} have been removed.")

        #Update Config File
        write_config(default_config)
        log_event(f"Configuration file changed: {bridge} removed.")

    except (FileNotFoundError, json.JSONDecodeError):
        print("Configuration file not found or invalid. Please create a bridge first.")
        log_event("During Remove Event: Configuration file not found or invalid. Please create a bridge first.")

def create_bridge_main():
    # log_event("bridge creation process started")
    
    interfaces = list_interfaces()
    print("Available interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i}: {iface}")

    try:
        idx1 = int(input("\nSelect the first interface by number: "))
        idx2 = int(input("\nSelect the second interface by number: "))
    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    if idx1 >= len(interfaces) or idx2 >= len(interfaces):
        print("\nInvalid interface number.")
        return

    interface1 = interfaces[idx1]
    interface2 = interfaces[idx2]

    create_bridge(interface1, interface2)
    #log_event(f"Bridge created with interfaces {interface1} and {interface2}.") # Redundant logging with create_bridge()
    print(f"\nBridge created with interfaces {interface1} and {interface2}.")
    
    log_event(show_bridge_info())
    show_bridge_info()

def main():
    read_config()  # Ensure the config file is created with empty fields
    
    while True:
        print("\n\n***** Bridge Utility *****")
        print()
        print("1. Create Bridge")
        print("2. Teardown Bridge")
        print("3. Show Interface Info")
        print("4. Exit")
        print()

        try:
            user_choice = int(input("Please make a selection: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if user_choice == 1:
            create_bridge_main()
        elif user_choice == 2:
            remove_bridge()
        elif user_choice == 3:
            show_bridge_info()
        elif user_choice == 4:
            exit()
        else:
            print("Invalid Option")
            continue

if __name__ == "__main__":
    log_event("Bridge Utility script started")
    main()
