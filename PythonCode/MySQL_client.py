import paho.mqtt.client as mqtt
import datetime
import json
import mysql.connector


class MySQL_client:
    def __init__(self, host, user, password, db):
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        self.db = self.mydb.cursor()

    def _fetchone(self,table,column):
        self.db.execute(f"SELECT {column} FROM {table} ORDER BY {column} desc LIMIT 1")
        return self.db.fetchone()[0]

    def update_data_table(self):
        sensor_id = self._fetchone("sensor", "sensor_id")
        payload_id = self._fetchone("payload", "payload_id")

        data_sql = "INSERT INTO data (payload_id,sensor_id) VALUES (%s,%s)"
        data_val = (payload_id, sensor_id)

        self.db.execute(data_sql, data_val)
        self.mydb.commit()
#
# def insert_querries():
#     payload_sql = "INSERT INTO payload (batV,bat_status,humidity,external_temp,internal_temp,received_at,airtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
#     sensor_sql = "INSERT INTO sensor (device_id,latitude,longitude,altitude) VALUES (%s,%s,%s,%s)"
#     return payload_sql, sensor_sql
