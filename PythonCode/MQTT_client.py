import paho.mqtt.client as mqtt
import datetime
import json
import mysql.connector
import MySQL_client

class MQTT_client:
    def __init__(self, subscriptions, sql_client, user, password, host):
        self.subscriptions = subscriptions
        self.sql_client = sql_client
        self.user = user
        self.password = password
        self.host = host
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        # Debug connection status
        print("Connected with result code " + str(rc))

        # Connecting to all the different sensors
        for sub in self.subscriptions:
            client.subscribe(sub)

        # client.subscribe("v3/project-software-engineering@ttn/devices/py-wierden/up")
        # client.subscribe("v3/project-software-engineering@ttn/devices/py-saxion/up")
        # client.subscribe("v3/project-software-engineering@ttn/devices/lht-wierden/up")
        # client.subscribe("v3/project-software-engineering@ttn/devices/lht-gronau/up")
        # client.subscribe("v3/project-software-engineering@ttn/devices/lht-saxion/up")

    def on_message(self, client, userdata, msg):
        # Parsing json data
        data = json.loads(msg.payload)

        # Getting device ID
        device_id = data['end_device_ids']['device_id']

        # SQL insert querries
        sensor_sql = "INSERT INTO sensor (device_id,latitude,longitude,altitude) VALUES (%s,%s,%s,%s)"

        # Payload talbe data recollection
        received_at = data['uplink_message']['received_at']
        received_at_decoded = received_at.split('.')[0]
        airtime = data['uplink_message']['consumed_airtime']
        airtime_decoded = airtime[0:8]

        if (device_id == 'py-saxion' or device_id == 'py-wierden'):
            temp = data['uplink_message']['decoded_payload']['temperature']
            light = data['uplink_message']['decoded_payload']['light']
            pres = data['uplink_message']['decoded_payload']['pressure']

            payload_sql = "INSERT INTO payload (internal_temp,pressure,light,received_at,airtime) VALUES (%s, %s, %s,%s,%s)"
            payload_val = (temp, pres, light, received_at_decoded, airtime_decoded)

        if (device_id == 'lht-wierden' or device_id == 'lht-gronau'):

            batV = data['uplink_message']['decoded_payload']['BatV']
            bat_status = data['uplink_message']['decoded_payload']['Bat_status']
            humidity = data['uplink_message']['decoded_payload']['Hum_SHT']
            light = data['uplink_message']['decoded_payload']['ILL_lx']
            external_temp = data['uplink_message']['decoded_payload']['TempC_SHT']

            payload_sql = "INSERT INTO payload (batV,bat_status,humidity,light,external_temp,received_at,airtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            payload_val = (batV, bat_status, humidity, light, external_temp, received_at_decoded, airtime_decoded)

        if (device_id == 'lht-saxion'):
            batV = data['uplink_message']['decoded_payload']['BatV']
            bat_status = data['uplink_message']['decoded_payload']['Bat_status']
            humidity = data['uplink_message']['decoded_payload']['Hum_SHT']
            external_temp = data['uplink_message']['decoded_payload']['TempC_DS']
            internal_temp = data['uplink_message']['decoded_payload']['TempC_SHT']

            payload_sql = "INSERT INTO payload (batV,bat_status,humidity,external_temp,internal_temp,received_at,airtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            payload_val = (batV, bat_status, humidity, external_temp, internal_temp, received_at_decoded, airtime_decoded)

        # Sensor table data recollection
        latitude = data['uplink_message']['rx_metadata'][0]['location']['latitude']
        longitude = data['uplink_message']['rx_metadata'][0]['location']['longitude']
        if (device_id != 'lht-gronau'):
            altitude = data['uplink_message']['rx_metadata'][0]['location']['altitude']
        else:
            altitude = None

        sensor_val = (device_id, latitude, longitude, altitude)

        self.sql_client.db.execute(payload_sql, payload_val)
        self.sql_client.db.execute(sensor_sql, sensor_val)
        self.sql_client.mydb.commit()

        self.sql_client.update_data_table()

        # Debug output
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}] {device_id}")

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.username_pw_set(self.user, self.password)
        self.client.connect(self.host, 1883, 60)

        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()


