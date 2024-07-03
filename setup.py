import psutil
import json
import subprocess

def list_interfaces():
    interfaces = psutil.net_if_addrs()
    return [iface for iface in interfaces if iface != 'lo']

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

def main():
    interfaces = list_interfaces()
    print("Available interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i}: {iface}")

    idx1 = int(input("Select the first interface by number: "))
    idx2 = int(input("Select the second interface by number: "))

    interface1 = interfaces[idx1]
    interface2 = interfaces[idx2]

    create_bridge(interface1, interface2)
    print(f"Bridge created with interfaces {interface1} and {interface2}.")

if __name__ == "__main__":
    main()
