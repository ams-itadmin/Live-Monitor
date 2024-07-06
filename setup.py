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


def remove_bridge():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Configuration file not found. Please create a bridge first.")
        return

    interface1, interface2 = config['interfaces']
    bridge = config['bridge']

    subprocess.run(['sudo', 'ip', 'link', 'set', interface1, 'promisc', 'off'])
    subprocess.run(['sudo', 'ip', 'link', 'set', interface2, 'promisc', 'off'])
    subprocess.run(['sudo', 'ip', 'link', 'set', bridge, 'down'])
    subprocess.run(['sudo', 'ip', 'link', 'delete', bridge, 'type', 'bridge'])

    print(f"Bridge {bridge} and promiscuous mode on {interface1} and {interface2} have been removed.")


def create_bridge_main():
    interfaces = list_interfaces()
    print("Available interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i}: {iface}")

    try:
        idx1 = int(input("Select the first interface by number: "))
        idx2 = int(input("Select the second interface by number: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if idx1 >= len(interfaces) or idx2 >= len(interfaces):
        print("Invalid interface number.")
        return

    interface1 = interfaces[idx1]
    interface2 = interfaces[idx2]

    create_bridge(interface1, interface2)
    print(f"Bridge created with interfaces {interface1} and {interface2}.")
    show_bridge_info()


def show_bridge_info():
    # Use subprocess to call brctl show
    result = subprocess.run(['brctl', 'show'], stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))

 #   # Use subprocess to call ip link show
 #   result = subprocess.run(['ip', 'link', 'show'], stdout=subprocess.PIPE)
 #   print(result.stdout.decode('utf-8'))

    # Use psutil to display network interface details
    interfaces = psutil.net_if_addrs()
    for iface, addrs in interfaces.items():
        print(f"Interface: {iface}")
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                print(f"MAC Address: {addr.address}")
        print("-" * 40)


def main():
    while True:
        print("***** Bridge Utility *****")
        print()
        print("1. Create Bridge")
        print("2. Teardown Bridge")
        print("3. Show Bridge Info")
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
    main()
