import paho.mqtt.client as mqtt
import datetime
import json
import MySQL_client

class MQTT_client:
    # Constructor
    def __init__(self, subscriptions, sql_client, user, password, host):
        # Initialize instance variables for mqtt connections
        self.subscriptions = subscriptions
        self.sql_client = sql_client
        self.user = user
        self.password = password
        self.host = host

        # Create an instance of the mqtt.Client class
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        """Called when the client successfully connects to the MQTT broker.
        Subscribes the client to all the topics in the subscriptions list."""
        # Debug connection status
        print("Connected with result code " + str(rc))

        # Connecting to all the different sensors
        for sub in self.subscriptions:
            client.subscribe(sub)

    def on_message(self, client, userdata, msg):
        """Called when the client receives a message from the MQTT broker.
        Parses the message payload as JSON and constructs an appropriate SQL INSERT query based on the device ID."""
        # Parsing json data
        data = json.loads(msg.payload)

        # Getting device ID
        device_id = data['end_device_ids']['device_id']

        # SQL insert querries
        sensor_sql = "INSERT INTO sensor (device_id,latitude,longitude,altitude) VALUES (%s,%s,%s,%s)"

        # Extract various data from the message payload
        received_at = data['uplink_message']['received_at']
        received_at_decoded = received_at.split('.')[0]
        airtime = data['uplink_message']['consumed_airtime']
        airtime_decoded = airtime[0:8]

        # Construct an appropriate SQL INSERT query based on the device ID
        if (device_id == 'py-saxion' or device_id == 'py-wierden'):
            temp = data['uplink_message']['decoded_payload']['temperature']
            light = data['uplink_message']['decoded_payload']['light']
            pres = data['uplink_message']['decoded_payload']['pressure']

            # Inserting data into the payload table
            payload_sql = "INSERT INTO payload (internal_temp,pressure,light,received_at,airtime) VALUES (%s, %s, %s,%s,%s)"
            payload_val = (temp, pres, light, received_at_decoded, airtime_decoded)


        if(device_id == 'eui-70b3d57ed00581d2'):
            humidity = data['uplink_message']['decoded_payload']['humdity']
            temp = data['uplink_message']['decoded_payload']['temperature']
            light = data['uplink_message']['decoded_payload']['light']
            pres = data['uplink_message']['decoded_payload']['pressure']

            # Inserting data into the payload table
            payload_sql = "INSERT INTO payload (humidity,internal_temp,pressure,light,received_at,airtime) VALUES (%s, %s, %s,%s,%s,%s)"
            payload_val = (humidity,temp, pres, light, received_at_decoded, airtime_decoded)

        if (device_id == 'lht-wierden' or device_id == 'lht-gronau'):
            batV = data['uplink_message']['decoded_payload']['BatV']
            bat_status = data['uplink_message']['decoded_payload']['Bat_status']
            humidity = data['uplink_message']['decoded_payload']['Hum_SHT']
            light = data['uplink_message']['decoded_payload']['ILL_lx']
            external_temp = data['uplink_message']['decoded_payload']['TempC_SHT']

            # Inserting data into the payload table
            payload_sql = "INSERT INTO payload (batV,bat_status,humidity,light,external_temp,received_at,airtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            payload_val = (batV, bat_status, humidity, light, external_temp, received_at_decoded, airtime_decoded)

        if (device_id == 'lht-saxion'):
            batV = data['uplink_message']['decoded_payload']['BatV']
            bat_status = data['uplink_message']['decoded_payload']['Bat_status']
            humidity = data['uplink_message']['decoded_payload']['Hum_SHT']
            external_temp = data['uplink_message']['decoded_payload']['TempC_DS']
            internal_temp = data['uplink_message']['decoded_payload']['TempC_SHT']

            # Inserting data into the payload table
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

        # Execute the SQL INSERT query
        self.sql_client.db.execute(payload_sql, payload_val)
        self.sql_client.db.execute(sensor_sql, sensor_val)
        self.sql_client.mydb.commit()

        # Update the data table
        self.sql_client.update_data_table()

        # Debug output
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}] {device_id}")

    def start(self):
        """Set the on_connect and on_message methods as callbacks for the client object,
        set the MQTT authentication details, and connect the client to the MQTT broker.
        Start the network loop to wait for incoming messages."""

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.username_pw_set(self.user, self.password)
        self.client.connect(self.host, 1883, 60)

        self.client.loop_start()

        if self.client.is_connected():
            print("Connected to MQTT broker")

    def stop(self):
        self.client.loop_stop()


