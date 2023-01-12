import json
import pytest
from MQTT_client import MQTT_client

# Create a mock SQL client object
class SQL_client_mock:
    def __init__(self):
        self.cursor = None

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
    assert mqtt_client.client.is_connected() == True

    # Test the on_message method with a test message payload
    msg = {
        "end_device_ids": {"device_id": "py-saxion"},
        "uplink_message": {
            "received_at": "2022-01-01T00:00:00.000000Z",
            "consumed_airtime": "1.23456789",
            "decoded_payload": {"temperature": 20, "light": 30, "pressure": 1013},
        },
    }
    msg_json = json.dumps(msg)
    client.on_message(mqtt_client, None, msg_json)
    sql_client.cursor.execute.assert_called_with(
        "INSERT INTO payload (internal_temp, pressure, light, received_at, airtime) VALUES (%s, %s, %s, %s, %s)",
        (20, 1013, 30, "2022-01-01T00:00:00", "1.234567"),
    )