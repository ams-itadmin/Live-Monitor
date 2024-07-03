# Live-Monitoring
 Live Monitor Network Traffic while being transparent to the network


## Purpose

This repository contains scripts to set up a network bridge and enable promiscuous mode on two network interfaces. 

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ams-itadmin/Live-Monitor.git
   cd Live-Monitor
   ```

1. Make the installer executable

    ```bash
    chmod +x installer.sh
    ```
1. Run the installer script:

    ```bash
    ./installer.sh
    ```

## Setup
1. Run the setup script to create the network bridge and enable promiscuous mode:

    ```bash
    python3 setup.py
    ```

1. Follow the prompts to select the two network interfaces.

## Teardown
1. Run the teardown script to remove the network bridge and disable promiscuous mode:

    ```bash
    python3 teardown.py
    ```