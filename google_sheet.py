import gspread
import os
import json
from google.oauth2.service_account import Credentials

# Google Sheet ID
SPREADSHEET_ID = "12S79JcWs7wn8WAanVRap11BmRD21AwobmvkEO-XOqCQ"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# JSON Key File
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

print("Google Sheet Connected Successfully")
from datetime import datetime

def update_google_sheet(devices):

    # Purana data delete karo
    sheet.clear()

    # Header
    sheet.append_row([
        "IP Address",
        "MAC Address",
        "Vendor",
        "Device Type",
        "Status",
        "Latency",
        "Last Seen"
    ])

    # Data
    for device in devices:

        last_seen = device.get(
            "last_seen",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        sheet.append_row([
            device["ip"],
            device["mac_address"],
            device["vendor"],
            device["device_type"],
            device["status"],
            str(device["latency"]),
            last_seen
        ])

    print("Google Sheet Updated Successfully")