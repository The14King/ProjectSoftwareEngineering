import json
import paho.mqtt.client as mqtt
import mock
import mysql
import pytest
from MQTT_client import MQTT_client

# Create a mock SQL client object
class SQL_client_mock:
    def __init__(self):
        # Connect to the MySQL database
        self.mydb = mysql.connector.connect(
            host="database.discordbothosting.com",
            user="u1604_6WUWgkmAxW",
            password="a3jXvb=fvbwOU=^3KQwO5s=b",
            database="s1604_ProjectSoftwareEngineering"
        )

        # Initialize a cursor object to execute queries
        self.db = self.mydb.cursor()
        self.cursor = self.db

    def update_data_table(self):
        pass

    def connect(self):
        pass

    def execute(self, query, values):
        pass

# Create a mock MQTT client object
class MQTT_client_mock:
    def __init__(self):
        self.connected = False

    def connect(self, host, port, keepalive):
        self.connected = True

    def subscribe(self, topic):
        pass

    def on_connect(self, callback):
        callback(self, None, None, 0)

    def on_message(self, callback):
        pass

def test_MQTT_client():
    # Create an instance of the MQTT client
    subscriptions = ["topic1", "topic2"]
    sql_client = SQL_client_mock()
    mqtt_client = MQTT_client_mock()
    client = MQTT_client(subscriptions, sql_client, "user", "password", "host")
    client.client = mqtt_client

    # Test the on_connect method
    client.on_connect(mqtt_client, None, None, 0)

    # Test the on_message method with a test message payload
    msg = mqtt.MQTTMessage()

    msg.payload = b'{"end_device_ids":{"device_id":"eui-70b3d57ed00581d2","application_ids":{"application_id":"group-1-project-software"},"dev_eui":"70B3D57ED00581D2","join_eui":"0000000000000000","dev_addr":"260BABEB"},"correlation_ids":["as:up:01GPZMAJ5EZ5F89XQPTH6KV715","ns:uplink:01GPZMAHYXZ7W5VQACV6VRQRWE","pba:conn:up:01GPNRV1161V87JQ7ZSZH0SADR","pba:uplink:01GPZMAHYT1NBMJ1VZ7JPJ4Y3C","rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01GPZMAHYXX3CJ3EQFDM3H49N9","rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01GPZMAJ5DWWX6S0FZV5JAY70C"],"received_at":"2023-01-17T10:27:46.989582596Z","uplink_message":{"session_key_id":"AYW/RSauACbI/+uaO9RMHA==","f_port":2,"frm_payload":"Ug1Gm2oA","decoded_payload":{"humdity":106,"light":155,"pressure":982,"temperature":20},"rx_metadata":[{"gateway_ids":{"gateway_id":"packetbroker"},"packet_broker":{"message_id":"01GPZMAHYT1NBMJ1VZ7JPJ4Y3C","forwarder_net_id":"000013","forwarder_tenant_id":"ttnv2","forwarder_cluster_id":"ttn-v2-legacy-eu","forwarder_gateway_eui":"AA555A000806053F","forwarder_gateway_id":"eui-aa555a000806053f","home_network_net_id":"000013","home_network_tenant_id":"ttn","home_network_cluster_id":"eu1.cloud.thethings.network"},"time":"2023-01-17T10:27:46.761405Z","rssi":-96,"channel_rssi":-96,"snr":9.5,"location":{"latitude":52.22121,"longitude":6.8857374,"altitude":66},"uplink_token":"eyJnIjoiWlhsS2FHSkhZMmxQYVVwQ1RWUkpORkl3VGs1VE1XTnBURU5LYkdKdFRXbFBhVXBDVFZSSk5GSXdUazVKYVhkcFlWaFphVTlwU2twUFNGcDFVek5hZFdKVVJrMVJhMmhDV1Zoa2RFbHBkMmxrUjBadVNXcHZhVkp0TVc5aU1sRjRWVVp3TlZveFZrMVZSelZUVkVkd2JWSlViREJhZVVvNUxtRndXbkJqYTJSWGN6WmZURVY0U0d0Q1dUVXRPWGN1VFZjd1VFSTRkalJ5ZGtveVUwRkdiUzQwZDA1aFNtSmtkMjFXVEcxVFVsTlJka3BsVUVWdWRtTTRWbEJsV1d4bFNWaG9UR1JPYjFsa2FESkdiR0ZsUld0Nk5sUnlVelpHUzNReWIzVkNkWEpUZFVOeFVreEJURGxCY3pGMVRqSm9VMmg1YTJ0c1JuQlBTVnBxZEZoQ2JqaFhZamRFWlhwSGFsQlpUbWRPYjBKc2VEQm5NVFY0VHpsUGRIbDRWMVkwT0VGMmRrRlpRblphTjFRemVqa3piV0YyYUdwS1NVUlJaV1pXWldsT1IzSXlhVlI0WkU5eVJubFRRMHRtYURrNExtcE5aMmRQUlhnNFdVdHRXbVZPU2pWS00yOTRTMUU9IiwiYSI6eyJmbmlkIjoiMDAwMDEzIiwiZnRpZCI6InR0bnYyIiwiZmNpZCI6InR0bi12Mi1sZWdhY3ktZXUifX0=","received_at":"2023-01-17T10:27:46.775831797Z"},{"gateway_ids":{"gateway_id":"centrum-enschede","eui":"AC1F09FFFE057EE0"},"time":"2023-01-17T10:27:46.779434919Z","timestamp":2638160151,"rssi":-74,"channel_rssi":-74,"snr":13.75,"location":{"latitude":52.2212025684184,"longitude":6.88635438680649,"altitude":70,"source":"SOURCE_REGISTRY"},"uplink_token":"Ch4KHAoQY2VudHJ1bS1lbnNjaGVkZRIIrB8J//4FfuAQl8L86QkaDAii8JmeBhDDlOn+AiDYg+X047QI","received_at":"2023-01-17T10:27:46.791543677Z"}],"settings":{"data_rate":{"lora":{"bandwidth":125000,"spreading_factor":7,"coding_rate":"4/5"}},"frequency":"868100000"},"received_at":"2023-01-17T10:27:46.781243985Z","consumed_airtime":"0.051456s","network_ids":{"net_id":"000013","tenant_id":"ttn","cluster_id":"eu1","cluster_address":"eu1.cloud.thethings.network"}}}'

    client.on_message(mqtt_client, None, msg)

    sql_client.cursor.execute(
        "INSERT INTO payload (internal_temp, pressure, light, received_at, airtime) VALUES (%s, %s, %s, %s, %s)",
        (20, 1013, 30, "2022-01-01T00:00:00", "1.234567"),
    )