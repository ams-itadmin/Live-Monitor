# Use a laptop to monitor traffic

## Purpose
Demonstrate how to monitor live traffic while mainintng transparcy to the network. This will be accomplished using Ubuntu, a laptop, a USB to RJ45 1Gbe adapter, and either WireShark or tcpdump.


## Overview
1. Prepare drive partition.
1. Install Ubuntu.
2. Install Wireshark.
3. Create bridge.
4. Use Wireshark to monitor bridge.


## Optional: Prepare Windows Laptop for Dual boot
Windows will usually fill the available partition on the drive. To install Ubuntu alongside Windows, you need to create space on the drive.

**Using Disk Management Tool**

1. Open Disk Management:
    - Press Win + X and select Disk Management.
    - Alternatively, press Win + R, type diskmgmt.msc, and press Enter.

1. Select the Partition:
    - In the Disk Management window, locate the partition you want to resize.

1. Shrink a Partition:
    - Right-click the partition you want to shrink and select Shrink Volume.
    - Enter the amount of space to shrink in MB and click Shrink.


## Install Ubuntu
1. Donwload the iso
2. Flash to a thumbdrive using `Balena Etcher` or `Rufus`
3. Boot laptop using USB
4. Follow install wizard
5. If dual booting, be very careful when selecting what partition to install on.



## Install required packages and software

1. Update repositories and the system.
    
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2. Install wireshark and tools

    ```bash
    sudo apt install wireshark bridge-utils net-utils -y
    ```
## Create the bridge
To create the bridge between the two interfaces, we need to know the what their names are. 

1. Find the interfaces using the following:

    ```bash
    ip a
    ```

    Example output

    ```
    itadmin@ThinkPad-E14:~$ ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host noprefixroute 
        valid_lft forever preferred_lft forever
    2: enp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
        link/ether 54:05:db:xx:xx:xx brd ff:ff:ff:ff:ff:ff
        inet 192.168.250.56/24 brd 192.168.250.255 scope global dynamic noprefixroute enp4s0
        valid_lft 41654sec preferred_lft 41654sec
    3: wlp5s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
        link/ether 30:c9:ab:xx:xx:xx brd ff:ff:ff:ff:ff:ff
        inet 192.168.20.109/24 brd 192.168.20.255 scope global dynamic noprefixroute wlp5s0
        valid_lft 84853sec preferred_lft 84853sec
        inet6 fe80::260:xxxx:xxxx:xxxx/64 scope link noprefixroute 
        valid_lft forever preferred_lft forever
    4: enx0050b6xxxxxx: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN group default qlen 1000
        link/ether 00:50:b6:xx:xx:xx brd ff:ff:ff:ff:ff:ff
    ```

    In the example output there are 4 interfaces, `lo` or `loopback`, `enp4s0`, `enx0050b6xxxxxx`, and `wlp5s0`. The names maybe different especially with USB adapters.

    In this example we would use `enp4s0` and `enx0050b6xxxxxx`, as `lo` is loopback address and won't help us out, and `wlp5s0` is the wireless adapter.


2. Create the bridge. Be sure to switch `<eth0>` and `<eth1>` for the actual interface names.
   
    ```bash   
    sudo ip link add br0 type bridge
    sudo ip link set <eth0> master br0
    sudo ip link set <eth1> master br0
    sudo ip link set br0 up
    sudo ip link set <eth0> promisc on
    sudo ip link set <eth1> promisc on
    sudo ip link set <eth0> up
    sudo ip link set <eth1> up
    ```

3. Check bridge interfaces
   
    ```bash
    # Check bridge interfaces
    sudo brctl show

    # Check link status and promiscuous mode
    sudo ip link show
    ```
    Example output:
    ```bash
    itadmin@ThinkPad-E14:~$ sudo brctl show
    bridge name	bridge id		STP enabled	interfaces
    br0		8000.fadd6c14ad7a	no		enp4s0
                                        enx0050b6xxxxxx
    ```



### Delete the existing bridge
After monitoring is complete you may want to destroy the bridge to regain the use of the interfaces.

1. To remove the bridge interface
    ```bash
    sudo ip link set br0 down
    sudo brctl delbr br0
    ```


## Capture traffic using `tcpdump`
Run tcpdump on the bridge interface to capture and analyze traffic.

```bash
sudo tcpdump -i br0 -w capture.pcap
```

## Capture and monitor traffic with WireShark
1. Open WireShark with `sudo`.
2. Select bridge interface to monitor.
3. Save and filter as needed.