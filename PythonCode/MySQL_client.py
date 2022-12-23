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
