import nmap
import psutil
import ipaddress
import socket
import subprocess
import re


from mac_vendor_lookup import MacLookup
from documentation import generate_report
from database import (
    delete_all_devices,
    update_device_status,
    mark_missing_devices_offline
)

# Current Network Track
current_network = None


# Auto Detect Network
def get_network_ranges():

    networks = []

    interfaces = psutil.net_if_addrs()

    for interface in interfaces.values():

        for addr in interface:

            if addr.family == socket.AF_INET:

                ip = addr.address

                if (
                    ip.startswith("127.")
                    or ip.startswith("169.254")
                ):
                    continue

                try:

                    parts = ip.split(".")

                    network = (
                        f"{parts[0]}."
                        f"{parts[1]}."
                        f"{parts[2]}.0/24"
                    )

                    if network not in networks:

                        networks.append(network)

                except:

                    pass

    return networks


# Get Latency
def get_latency(ip):

    try:

        result = subprocess.check_output(
            ["ping", "-n", "1", ip],
            universal_newlines=True
        )

        match = re.search(
            r"time[=<](\d+)ms",
            result
        )

        if match:
            return int(match.group(1))

        return 0

    except:

        return 0


# Vendor Detection
def get_vendor(mac_address):

    try:

        if mac_address == "Unknown":
            return "Unknown Vendor"

        return MacLookup().lookup(
            mac_address
        )

    except:

        return "Unknown Vendor"


# Device Type Detection
def get_device_type(hostname, vendor):

    hostname = hostname.lower()

    if "desktop" in hostname:
        return "Desktop"

    elif "pc" in hostname:
        return "Desktop"

    elif "laptop" in hostname:
        return "Laptop"

    elif "android" in hostname:
        return "Mobile"

    elif "iphone" in hostname:
        return "Mobile"

    elif "router" in hostname:
        return "Router"

    elif "apple" in vendor.lower():
        return "Mobile"

    elif "samsung" in vendor.lower():
        return "Mobile"

    elif "dell" in vendor.lower():
        return "Laptop"

    elif "hp" in vendor.lower():
        return "Laptop"

    elif "lenovo" in vendor.lower():
        return "Laptop"

    elif "asus" in vendor.lower():
        return "Laptop"

    elif "tp-link" in vendor.lower():
        return "Router"

    elif "cisco" in vendor.lower():
        return "Switch"

    else:
        return "Network Device"


# Main Scan Function
def scan_network():

    global current_network

    devices = []

    networks = get_network_ranges()

    for network in networks:

     print(f"\nScanning Network : {network}")
     scanner = nmap.PortScanner()

    scanner.scan(
      network,
    arguments='-sn -T5 --min-parallelism 100'
)
    # Network Change Detection
    if current_network is None:

        current_network = network

    elif current_network != network:

        print("\nNetwork Changed!")

        print(
            f"Old Network: {current_network}"
        )

        print(
            f"New Network: {network}"
        )

        delete_all_devices()

        current_network = network

    


    found_ips = []

    for host in scanner.all_hosts():

        found_ips.append(host)

        try:

            hostname = scanner[host].hostname()

        except:

            hostname = ""

        try:

            mac_address = scanner[host][
                'addresses'
            ].get(
                'mac',
                'Unknown'
            )

        except:

            mac_address = "Unknown"

        vendor = get_vendor(
            mac_address
        )

        device_type = get_device_type(
            hostname,
            vendor
        )

        # Fast Mode
        latency = get_latency(host)

        # Agar latency chahiye:
        # latency = get_latency(host)

        print(
            f"IP: {host} | "
            f"MAC: {mac_address} | "
            f"Vendor: {vendor} | "
            f"Type: {device_type}"
        )

        devices.append({

            "ip": host,
            "status": "Online",
            "latency": latency,
            "device_type": device_type,
            "mac_address": mac_address,
            "vendor": vendor

        })

        try:

            update_device_status(
                host,
                "Online",
                latency,
                device_type,
                mac_address,
                vendor
            )

        except Exception as e:

            print(
                "Database Error:",
                e
            )

    # Offline Detection
    mark_missing_devices_offline(
        found_ips
    )
    generate_report(devices)

    return devices


if __name__ == "__main__":

    # Vendor Database Update
    try:

        MacLookup().update_vendors()

    except:

        pass

    devices = scan_network()

    print("\nDevices Found:\n")

    for device in devices:

        print(device)

    print(
        f"\nTotal Devices Found: {len(devices)}"
    )

    print(
        "\nScan Completed Successfully"
    )