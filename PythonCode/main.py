from MySQL_client import MySQL_client
from MQTT_client import MQTT_client

# Initialize a MySQL client
sql_client = MySQL_client("database.discordbothosting.com",
                          "u1604_6WUWgkmAxW",
                          "a3jXvb=fvbwOU=^3KQwO5s=b",
                          "s1604_ProjectSoftwareEngineering")

# subscription list for first client
subscriptions1 = ["v3/project-software-engineering@ttn/devices/py-wierden/up",
                  "v3/project-software-engineering@ttn/devices/py-saxion/up",
                  "v3/project-software-engineering@ttn/devices/lht-wierden/up",
                  "v3/project-software-engineering@ttn/devices/lht-gronau/up",
                  "v3/project-software-engineering@ttn/devices/lht-saxion/up"]
# subscription list for second client
subscriptions2 = ["v3/group-1-project-software@ttn/devices/eui-70b3d57ed00581d2/up"]

# Initialize a MQTT client
mqtt_client1 = MQTT_client(subscriptions1, sql_client,
                           "project-software-engineering@ttn",
                           "NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA",
                           "eu1.cloud.thethings.network")
mqtt_client2 = MQTT_client(subscriptions2, sql_client,
                           "group-1-project-software@ttn",
                           "NNSXS.U2ZBDOUHEIAQ6WGOOZH44PNDYE7NHT2PNQFEXXY.VZ6HGVZQW4DCQB3DJHWI4CTPIQB2PVRLB7MYSU7CCODBHU6TQGBA",
                           "eu1.cloud.thethings.network")

# Connect to the MQTT broker
mqtt_client1.start()
mqtt_client2.start()

# Keep the main thread alive
while True:
    x = input("$: ")
    if x == 'quit' or x == 'q' or x == 'exit':
        break

# Disconnect from the MQTT broker
mqtt_client1.stop()
mqtt_client2.stop()