import mysql.connector
import random
from datetime import datetime

config = {
    'user': 'ktong1',
    'password': 'pw',
    'host': 'localhost',
    'database': 'ktong1'
}

# dictionary of dorms of dictionary of class of list of netids
students = {}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# obtain all netID
query = ("SELECT netID, dorm_name, class from Students")

cursor.execute(query)

i = 0

for (netID, dorm_name, classS) in cursor:
    if students.get(dorm_name) == None:
        students[dorm_name] = {'FR': [], 'SO': [], 'JR': []}
    students[dorm_name][classS].append(netID)

# shuffle the netIDs
for dorm, years in students.iteritems():
    pick_num = 1
    random.shuffle(years['FR'])
    random.shuffle(years['SO'])
    random.shuffle(years['JR'])

    for jr in years['JR']:
        add_pick = ("INSERT INTO Picks (dorm_name, pick, netID) VALUES (%s, %s, %s)")
        data_pick = (dorm, pick_num, jr)
        cursor.execute(add_pick, data_pick)
        pick_num += 1

    for so in years['SO']:
        add_pick = ("INSERT INTO Picks (dorm_name, pick, netID) VALUES (%s, %s, %s)")
        data_pick = (dorm, pick_num, so)
        cursor.execute(add_pick, data_pick)
        pick_num += 1

    for fr in years['FR']:
        add_pick = ("INSERT INTO Picks (dorm_name, pick, netID) VALUES (%s, %s, %s)")
        data_pick = (dorm, pick_num, fr)
        cursor.execute(add_pick, data_pick)
        pick_num += 1

    cnx.commit()

cursor.close()
cnx.close()

