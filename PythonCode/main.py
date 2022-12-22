from pprint import pprint

import paho.mqtt.client as mqtt
import datetime
import json
import mysql.connector


def sensor_query():
    query = "INSERT INTO sensor (device_id,latitude,longitude,altitude) VALUES (%s,%s,%s,%s)"
    return query


def print_device(device_id):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {device_id}")


def lht_sensor_msg(mydb, db, test, device_id):
    # SQL insert queries
    payload_sql = "INSERT INTO payload (batV,bat_status,humidity,light,external_temp,received_at,airtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    sensor_sql = sensor_query()

    # Payload table data recollection
    batV = test['uplink_message']['decoded_payload']['BatV']
    bat_status = test['uplink_message']['decoded_payload']['Bat_status']
    humidity = test['uplink_message']['decoded_payload']['Hum_SHT']
    light = test['uplink_message']['decoded_payload']['ILL_lx']
    external_temp = test['uplink_message']['decoded_payload']['TempC_SHT']
    received_at = test['uplink_message']['received_at']
    received_at_decoded = received_at.split('.')[0]
    airtime = test['uplink_message']['consumed_airtime']
    airtime_decoded = airtime[0:8]

    # Sensor table data recollection
    if (device_id == 'lht-gronau'):
        latitude = test['uplink_message']['rx_metadata'][0]['location']['latitude']
        longitude = test['uplink_message']['rx_metadata'][0]['location']['longitude']
        altitude = None
    else:
        latitude, longitude, altitude = sensor_table_data(test)

    # Data grouping
    payload_val = (batV, bat_status, humidity, light, external_temp, received_at_decoded, airtime_decoded)
    sensor_val = (device_id, latitude, longitude, altitude)

    # SQL queries execution
    db.execute(payload_sql, payload_val)
    db.execute(sensor_sql, sensor_val)
    mydb.commit()

    # Data table
    update_data_table(mydb, db)

    # Debugging output
    print_device(device_id)


def py_sensor_msg(mydb, db, test, device_id):
    # SQL insert queries
    sensor_sql = sensor_query()
    payload_sql = "INSERT INTO payload (internal_temp,pressure,light,received_at,airtime) VALUES (%s, %s, %s,%s,%s)"

    # Payload table data recollection
    temp = test['uplink_message']['decoded_payload']['temperature']
    light = test['uplink_message']['decoded_payload']['light']
    pres = test['uplink_message']['decoded_payload']['pressure']
    received_at = test['uplink_message']['received_at']
    received_at_decoded = received_at.split('.')[0]
    airtime = test['uplink_message']['consumed_airtime']
    airtime_decoded = airtime[0:8]

    #Sensor table data
    latitude, longitude, altitude = sensor_table_data(test)

    # Data grouping
    sensor_val = (device_id, latitude, longitude, altitude)
    payload_val = (temp, pres, light, received_at_decoded, airtime_decoded)

    # SQL queries execution
    db.execute(payload_sql, payload_val)
    db.execute(sensor_sql, sensor_val)
    mydb.commit()

    # Data table
    update_data_table(mydb, db)

    # Debugging output
    print_device(device_id)


def sensor_table_data(test):
    # Sensor table data recollection
    latitude = test['uplink_message']['rx_metadata'][0]['location']['latitude']
    longitude = test['uplink_message']['rx_metadata'][0]['location']['longitude']
    altitude = test['uplink_message']['rx_metadata'][0]['location']['altitude']

    return latitude,longitude,altitude


def update_data_table(mydb, db):
    data_sql = "INSERT INTO data (payload_id,sensor_id) VALUES (%s,%s)"

    db.execute("SELECT sensor_id FROM sensor ORDER BY sensor_id desc LIMIT 1")
    sensor_id = db.fetchone()[0]
    db.execute("SELECT payload_id FROM payload ORDER BY payload_id desc LIMIT 1")
    payload_id = db.fetchone()[0]
    data_val = (payload_id, sensor_id)
    db.execute(data_sql, data_val)
    mydb.commit()


def on_connect(client, userdata, flags, rc):
    # Debug connection status
    print("Connected with result code " + str(rc))

    # Connecting to all the different sensors
    client.subscribe("v3/project-software-engineering@ttn/devices/py-wierden/up")
    client.subscribe("v3/project-software-engineering@ttn/devices/py-saxion/up")
    client.subscribe("v3/project-software-engineering@ttn/devices/lht-wierden/up")
    client.subscribe("v3/project-software-engineering@ttn/devices/lht-gronau/up")
    client.subscribe("v3/project-software-engineering@ttn/devices/lht-saxion/up")


# def on_connect2(client, userdata, flags, rc):
#     # Debug connection status
#     print("Connected with result code " + str(rc))
#
#     # Connecting to all the different sensors
#     client.subscribe("#")


def on_message(client, userdata,msg):
    # Parsing json data
    test = json.loads(msg.payload)

    # Getting device ID
    device_id = test['end_device_ids']['device_id']

    # SQL connection
    mydb = mysql.connector.connect(
        host="database.discordbothosting.com",
        user="u1604_6WUWgkmAxW",
        password="a3jXvb=fvbwOU=^3KQwO5s=b",
        database="s1604_ProjectSoftwareEngineering"
    )
    db = mydb.cursor()

    # Different data recollection depending on the device
    if(device_id == 'py-saxion' or device_id == 'py-wierden'):
        py_sensor_msg(mydb, db, test, device_id)


    if(device_id == 'lht-wierden' or device_id == 'lht-gronau'):
        lht_sensor_msg(mydb, db, test, device_id)

    if (device_id == 'lht-saxion'):
        # SQL insert querries
        payload_sql = "INSERT INTO payload (batV,bat_status,humidity,external_temp,internal_temp,received_at,airtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        sensor_sql = sensor_query()

        # Payload table data recollection
        batV = test['uplink_message']['decoded_payload']['BatV']
        bat_status = test['uplink_message']['decoded_payload']['Bat_status']
        humidity = test['uplink_message']['decoded_payload']['Hum_SHT']
        external_temp = test['uplink_message']['decoded_payload']['TempC_DS']
        internal_temp = test['uplink_message']['decoded_payload']['TempC_SHT']
        received_at = test['uplink_message']['received_at']
        received_at_decoded = received_at.split('.')[0]
        airtime = test['uplink_message']['consumed_airtime']
        airtime_decoded = airtime[0:8]

        # Sensor table data recollection
        latitude, longitude, altitude = sensor_table_data(test)

        # Data grouping
        payload_val = (batV, bat_status, humidity, external_temp, internal_temp, received_at_decoded, airtime_decoded)
        sensor_val = (device_id, latitude, longitude, altitude)

        # SQL queries execution
        db.execute(payload_sql, payload_val)
        db.execute(sensor_sql, sensor_val)
        mydb.commit()

        # Data table
        update_data_table(mydb, db)

        # Debug output
        print_device(device_id)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('project-software-engineering@ttn', 'NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA')
client.connect("eu1.cloud.thethings.network", 1883, 60)

# client2 = mqtt.Client()
# client2.on_connect = on_connect2
# client2.on_message = on_message
# client2.username_pw_set('group-1-project-software@ttn', 'NNSXS.U2ZBDOUHEIAQ6WGOOZH44PNDYE7NHT2PNQFEXXY.VZ6HGVZQW4DCQB3DJHWI4CTPIQB2PVRLB7MYSU7CCODBHU6TQGBA')
# client2.connect("eu1.cloud.thethings.network", 1883, 60)

#The loop cheking for new payload and after formating prints the needed information
client.loop_start()
# client2.loop_start()

while True:
    None
