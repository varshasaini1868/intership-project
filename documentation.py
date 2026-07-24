import os
import csv
from datetime import datetime


def generate_report(devices):

    folder = "Railway_Network_Documents"

    os.makedirs(folder, exist_ok=True)

    current_time = datetime.now()

    filename = "Network_Report.txt"

    filepath = os.path.join(
        folder,
        filename
    )

    # ---------------- TXT REPORT ----------------

    with open(filepath, "w") as file:

        file.write("RAILWAY NETWORK REPORT\n")
        file.write("=" * 50 + "\n\n")

        file.write(
            f"Generated Time : {current_time}\n\n"
        )

        file.write(
            f"Total Devices : {len(devices)}\n\n"
        )

        for device in devices:

            file.write(
                f"IP Address : {device['ip']}\n"
            )

            file.write(
                f"MAC Address : {device['mac_address']}\n"
            )

            file.write(
                f"Vendor : {device['vendor']}\n"
            )

            file.write(
                f"Device Type : {device['device_type']}\n"
            )

            file.write(
                f"Status : {device['status']}\n"
            )

            file.write(
                f"Latency : {device['latency']} ms\n"
            )

            file.write(
                "-" * 40 + "\n"
            )

    print("TXT Report Saved :", filepath)

    # ---------------- CSV REPORT ----------------

    csv_file = os.path.join(
        folder,
        "devices.csv"
    )

    with open(csv_file, "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "IP Address",
            "MAC Address",
            "Vendor",
            "Device Type",
            "Status",
            "Latency"
        ])

        for device in devices:

            writer.writerow([

                device["ip"],
                device["mac_address"],
                device["vendor"],
                device["device_type"],
                device["status"],
                device["latency"]

            ])

    print("CSV Report Saved :", csv_file)
  