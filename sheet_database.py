import os
import json
import gspread
from google.oauth2.service_account import Credentials

# -------------------------
# Google Sheet Configuration
# -------------------------

SPREADSHEET_ID = "12S79JcWs7wn8WAanVRap11BmRD21AwobmvkEO-XOqCQ"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Read credentials from Render Environment Variable
google_credentials = os.getenv("GOOGLE_CREDENTIALS")

if not google_credentials:
    raise Exception("GOOGLE_CREDENTIALS environment variable not found.")

credentials_info = json.loads(google_credentials)

credentials = Credentials.from_service_account_info(
    credentials_info,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

sheet = client.open_by_key(SPREADSHEET_ID).sheet1


# -------------------------
# Read Devices from Google Sheet
# -------------------------

def get_devices():

    records = sheet.get_all_records()

    devices = []

    for index, row in enumerate(records, start=1):

        latency = 0

        try:
            latency = int(row.get("Latency", 0))
        except:
            latency = 0

        devices.append({

            "id": index,

            "ip": row.get("IP Address", ""),

            "mac_address": row.get("MAC Address", ""),

            "vendor": row.get("Vendor", ""),

            "device_type": row.get("Device Type", ""),

            "status": row.get("Status", "Offline"),

            "latency": latency,

            "last_seen": row.get("Last Seen", "")

        })

    return devices


# -------------------------
# Dashboard Summary
# -------------------------

def get_devices_for_dashboard():

    devices = get_devices()

    total = len(devices)

    online = sum(
        1 for d in devices
        if str(d["status"]).lower() == "online"
    )

    offline = total - online

    if total > 0:
        health = round((online / total) * 100, 2)
    else:
        health = 0

    online_devices = [
        d for d in devices
        if str(d["status"]).lower() == "online"
    ]

    if online_devices:

        avg_latency = round(
            sum(d["latency"] for d in online_devices)
            / len(online_devices),
            2
        )

    else:

        avg_latency = 0

    return {

        "devices": devices,

        "total": total,

        "online": online,

        "offline": offline,

        "health": health,

        "avg_latency": avg_latency

    }