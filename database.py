import mysql.connector

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="railway_network"
)

cursor = conn.cursor(dictionary=True)

print("Database Connected Successfully")


# Delete All Devices
def delete_all_devices():

    query = """
    DELETE FROM devices
    """

    cursor.execute(query)

    conn.commit()


# Update Device Status
def update_device_status(
        ip,
        status,
        latency=0,
        device_type="Unknown",
        mac_address="Unknown",
        vendor="Unknown Vendor"
):

    query = """
    INSERT INTO devices
    (
        ip,
        status,
        latency,
        device_type,
        mac_address,
        vendor
    )

    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )

    ON DUPLICATE KEY UPDATE

        status = VALUES(status),
        latency = VALUES(latency),
        device_type = VALUES(device_type),
        mac_address = VALUES(mac_address),
        vendor = VALUES(vendor),
        last_seen = CURRENT_TIMESTAMP
    """

    cursor.execute(
        query,
        (
            ip,
            status,
            latency,
            device_type,
            mac_address,
            vendor
        )
    )

    conn.commit()


# Offline Detection
def mark_missing_devices_offline(found_ips):

    if not found_ips:
        return

    placeholders = ",".join(
        ["%s"] * len(found_ips)
    )

    query = f"""
    UPDATE devices

    SET
        status='Offline',
        latency=0

    WHERE ip NOT IN ({placeholders})
    """

    cursor.execute(
        query,
        tuple(found_ips)
    )

    conn.commit()


# Get All Devices
def get_devices():

    query = """
    SELECT *
    FROM devices
    ORDER BY ip
    """

    cursor.execute(query)

    return cursor.fetchall()


# Dashboard Data
def get_devices_for_dashboard():

    devices = get_devices()

    total = len(devices)

    online = sum(
        1 for device in devices
        if device["status"] == "Online"
    )

    offline = sum(
        1 for device in devices
        if device["status"] == "Offline"
    )

    online_devices = [

        device

        for device in devices

        if device["status"] == "Online"

    ]

    if len(online_devices) > 0:

        avg_latency = round(

            sum(
                device["latency"]

                for device in online_devices
            )

            /

            len(online_devices),

            2

        )

    else:

        avg_latency = 0

    return {

        "total": total,

        "online": online,

        "offline": offline,

        "avg_latency": avg_latency,

        "devices": devices

    }


# Testing
if __name__ == "__main__":

    devices = get_devices()

    print("\nDevices Found:\n")

    for device in devices:

        print(device)

    conn.close()