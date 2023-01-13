import mysql.connector


class MySQL_client:
    def __init__(self, host, user, password, db):
        # Connect to the MySQL database
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )

        # Initialize a cursor object to execute queries
        self.db = self.mydb.cursor()

    def _fetchone(self,table,column):
        # Fetch the latest entry in the specified table, sorted by the specified column in descending order
        self.db.execute(f"SELECT {column} FROM {table} ORDER BY {column} desc LIMIT 1")
        return self.db.fetchone()[0]

    def update_data_table(self):
        # Fetch the latest sensor_id and payload_id from the sensor and payload tables, respectively
        sensor_id = self._fetchone("sensor", "sensor_id")
        payload_id = self._fetchone("payload", "payload_id")

        # Prepare an INSERT statement to insert a new row into the data table
        data_sql = "INSERT INTO data (payload_id,sensor_id) VALUES (%s,%s)"
        # Specify the values to be inserted into the new row
        data_val = (payload_id, sensor_id)

        # Execute the SQL INSERT query
        self.db.execute(data_sql, data_val)
        self.mydb.commit()

    def reconnect(self):
        return self.mydb.ping(reconnect=True, attempts=1, delay=0)
