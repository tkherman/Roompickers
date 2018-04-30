import mysql.connector
import random
from datetime import datetime

config = {
    'user': 'ktong1',
    'password': 'pw',
    'host': 'localhost',
    'database': 'ktong1'
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# obtain all netID
query = ("SELECT dorm_name, pick, netID from Picks")

cursor.execute(query)

data = []
for (dorm_name, pick, netID) in cursor:
    data.append((dorm_name, pick, netID))

for d in data:
    update = ("UPDATE Picks SET start = '2018-05-20 20:00:00', END = '2018-05-20 21:00:00' "
                    "WHERE dorm_name = %s and pick = %s and netID = %s")
    cursor.execute(update, (d[0], d[1], d[2],))

cnx.commit()
cursor.close()
cnx.close()

