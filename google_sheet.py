import gspread
from google.oauth2.service_account import Credentials

# Google Sheet ID
SPREADSHEET_ID = "12S79JcWs7wn8WAanVRap11BmRD21AwobmvkEO-XOqCQ"

# JSON Key File
SERVICE_ACCOUNT_FILE = "ai-railway-network-management-c3fa26bcfd8a.json"

# Permissions
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
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