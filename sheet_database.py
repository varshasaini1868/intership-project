import os
import json
import gspread

from google.oauth2.service_account import Credentials

# -------------------------
# Google Sheet Configuration
# -------------------------

SPREADSHEET_ID = "12S79JcWs7wn8WAanVRap11BmRD21AwobmvkEO-XOqCQ"

google_credentials = os.getenv("GOOGLE_CREDENTIALS")

if google_credentials:

    credentials_info = json.loads(google_credentials)

    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

else:

    credentials = Credentials.from_service_account_file(
        "ai-railway-network-management-c3fa26bcfd8a.json",
        scopes=SCOPES
    )

client = gspread.authorize(credentials)

sheet = client.open_by_key(SPREADSHEET_ID).sheet1


# -------------------------
# Get Devices
# -------------------------

def get_devices():

    records = sheet.get_all_records()

    devices = []

    for row in records:

        devices.append({

            "id": len(devices) + 1,

            "ip": row["IP Address"],

            "mac_address": row["MAC Address"],

            "vendor": row["Vendor"],

            "device_type": row["Device Type"],

            "status": row["Status"],

            "latency": int(row["Latency"]) if str(row["Latency"]).isdigit() else 0,

            "last_seen": row["Last Seen"]

        })

    return devices


# -------------------------
# Dashboard Data
# -------------------------

def get_devices_for_dashboard():

    devices = get_devices()

    total = len(devices)

    online = sum(
        1 for d in devices
        if d["status"] == "Online"
    )

    offline = total - online

    health = 0

    if total > 0:

        health = round(
            (online / total) * 100,
            1
        )

    avg_latency = 0

    if online > 0:

        avg_latency = round(

            sum(
                d["latency"]

                for d in devices

                if d["status"] == "Online"

            )

            /

            online,

            1

        )

    return {

        "total": total,

        "online": online,

        "offline": offline,

        "health": health,

        "avg_latency": avg_latency,

        "devices": devices

    }


# -------------------------
# Testing
# -------------------------

if __name__ == "__main__":

    data = get_devices_for_dashboard()

    print(data)