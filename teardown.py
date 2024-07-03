import json
import subprocess

def remove_bridge():
    with open('config.json', 'r') as f:
        config = json.load(f)

    interface1, interface2 = config['interfaces']
    bridge = config['bridge']

    subprocess.run(['sudo', 'ip', 'link', 'set', interface1, 'promisc', 'off'])
    subprocess.run(['sudo', 'ip', 'link', 'set', interface2, 'promisc', 'off'])
    subprocess.run(['sudo', 'ip', 'link', 'set', bridge, 'down'])
    subprocess.run(['sudo', 'ip', 'link', 'delete', bridge, 'type', 'bridge'])

    print(f"Bridge {bridge} and promiscuous mode on {interface1} and {interface2} have been removed.")

def main():
    remove_bridge()

if __name__ == "__main__":
    main()
