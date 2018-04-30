from flask import Flask, request
import mysql.connector
import json
import sys
import os
app = Flask(__name__)


# Return available room list
@app.route('/floors/images/<netID>/<dorm_name>')
def get_floorplans(netID, dorm_name):
    split = dorm_name.split()
    split = ''.join(split)
    path = 'data/floorplans/' + split;
    files = os.popen('ls ' + path).read();
    filenames = files.split()

    # dorm_name is first value in list
    filenames.insert(0, dorm_name);
    return json.dumps(filenames);

# Return available room list
@app.route('/floors/<netID>/<dorm_name>')
def get_rooms(netID, dorm_name):
    mens_dorm = ['Alumni', 'Carroll', 'Dillon', 'Duncan', 'Dunne', 'Fisher',
                 'Keenan', 'Keough', 'Knott', 'Morrissey', 'O\'Neil Family',
                 'Siegfried', 'Sorin', 'St. Edward\'s', 'Stanford', 'Zahm']
    womens_dorm = ['Badin', 'Breen-Phillips', 'Cavanaugh', 'Farley', 'Flaherty',
                   'Howard', 'Lewis', 'Lyons', 'McGlinn', 'Pasquerilla East',
                   'Pasquerilla West', 'Ryan', 'Walsh', 'Welsh Family']

    if dorm_name not in mens_dorm and dorm_name not in womens_dorm:
        return "Invalid dorm name"

    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    query = ("SELECT r.dorm_name, r.floor_num, r.room_num, r.size, r.capacity, r.available "
            "FROM Rooms r, Selections s "
            "WHERE r.dorm_name = %s and (r.dorm_name <> s.dorm_name or "
                "r.room_num <> s.room_num)")

    cursor.execute(query, (dorm_name,))

    data = {"rooms": []}

    for i in cursor:
        room = {}
        room['dorm_name'] = i[0]
        room['floor_num'] = i[1]
        room['room_num'] = i[2]
        room['size'] = i[3]
        room['capacity'] = i[4]
        room['available'] = i[5]
        data['rooms'].append(room)

    cursor.close()
    cnx.close()

    return json.dumps(data)

# Returns filtered room list
@app.route('/filter/<netID>/<dorm_name>/<capacity>/<size_min>/<size_max>')
def filter_rooms(netID, dorm_name, capacity, size_min, size_max): #add size filter
    mens_dorm = ['Alumni', 'Carroll', 'Dillon', 'Duncan', 'Dunne', 'Fisher',
                 'Keenan', 'Keough', 'Knott', 'Morrissey', 'O\'Neil Family',
                 'Siegfried', 'Sorin', 'St. Edward\'s', 'Stanford', 'Zahm']
    womens_dorm = ['Badin', 'Breen-Phillips', 'Cavanaugh', 'Farley', 'Flaherty',
                   'Howard', 'Lewis', 'Lyons', 'McGlinn', 'Pasquerilla East',
                   'Pasquerilla West', 'Ryan', 'Walsh', 'Welsh Family']

    if dorm_name not in mens_dorm and dorm_name not in womens_dorm:
        return "Invalid dorm name"

    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    # this query does not filter by floot num
    query = ("SELECT r.dorm_name, r.floor_num, r.room_num, r.size, r.capacity, r.available "
             "FROM Rooms r, Selections s "
             "WHERE r.dorm_name = %s and (r.dorm_name <> s.dorm_name or "
             "r.room_num <> s.room_num) and r.capacity <= %s and "
             "r.size >= %s and r.size <= %s")
    cursor.execute(query, (dorm_name, capacity, size_min, size_max))

    data = {"rooms": []}

    for i in cursor:
        room = {}
        room['dorm_name'] = i[0]
        room['floor_num'] = i[1]
        room['room_num'] = i[2]
        room['size'] = i[3]
        room['capacity'] = i[4]
        room['available'] = i[5]
        data['rooms'].append(room)

    cursor.close()
    cnx.close()

    return json.dumps(data)

# Return min max floor numbers and min max size
@app.route('/floor_metadata/<netID>/<dorm_name>/')
def floor_metadata(netID, dorm_name):
    min_floor = None
    max_floor = None
    min_size = None
    max_size = None

    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    query = ("SELECT size FROM Rooms WHERE dorm_name = %s ORDER BY size LIMIT 1")
    cursor.execute(query, (dorm_name,))

    for i in cursor:
        min_size = i[0]

    query = ("SELECT size FROM Rooms WHERE dorm_name = %s ORDER BY size DESC LIMIT 1")
    cursor.execute(query, (dorm_name,))

    for i in cursor:
        max_size = i[0]

    query = ("SELECT floor_num FROM Rooms WHERE dorm_name = %s ORDER BY floor_num LIMIT 1")
    cursor.execute(query, (dorm_name,))

    for i in cursor:
        min_floor = i[0]

    query = ("SELECT floor_num FROM Rooms WHERE dorm_name = %s ORDER BY floor_num DESC LIMIT 1")
    cursor.execute(query, (dorm_name,))

    for i in cursor:
        max_floor = i[0]

    data = {'min_size': min_size, 'max_size': max_size, 'min_floor': min_floor, 'max_floor': max_floor}

    return json.dumps(data)

# Return selection time for specified student
@app.route('/time/<netID>/<dorm_name>/')
def selection_time(netID):
    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    query = ("SELECT start, end FROM Picks WHERE dorm_name = %s and netID = %s")
    cursor.execute(query, (dorm_name, netID,))

    data = {}

    for i in cursor:
        data['start'] = i[0]
        data['end'] = i[1]

    return json.dumps(data)

@app.route('/rooms/<netID>/<dorm>')
def query_rooms(netID, dorm):
    # tmp file for dummy json data
    filename = '/home/cse30246/aborowsk/tests/test.json'
    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)


    return json.dumps(data)

@app.route('/preferences/<netID>/<dorm>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def query_preferences(netID, dorm):
    if request.method == 'GET':
        data = {'preferences': []}

        cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
        cursor = cnx.cursor()

        query = ("SELECT netID, pref_num, room, dorm_name, rm1, rm2, rm3 "
                 "FROM Preferences "
                 "WHERE netID = %s "
                 "ORDER BY pref_num")
        cursor.execute(query, (netID,))

        for i in cursor:
            pref = {}
            pref['netID'] = i[0]
            pref['pref_num'] = i[1]
            pref['room'] = i[2]
            pref['dorm_name'] = i[3]

            if i[4] != None:
                pref['rm1'] = i[4]
            else:
                pref['rm1'] = '---'

            if i[5] != None:
                pref['rm2'] = i[5]
            else:
                pref['rm2'] = '---'

            if i[6] != None:
                pref['rm3'] = i[6]
            else:
                pref['rm3'] = '---'

            data['preferences'].append(pref)

        return json.dumps(data)

    if request.method == 'POST':
        data = request.data
        preferences = json.loads(data)

        cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
        cursor = cnx.cursor()

        # Check that all netID are in Students and all rooms are in Rooms
        # if not, return error
        students = set()
        rooms = set()
        for pref in preferences['preferences']:
            rooms.add((pref['dorm_name'], pref['room']))
            if pref['rm1'] != '---':
                students.add(pref['rm1'])
            else:
                pref['rm1'] = None

            if pref['rm2'] != '---':
                students.add(pref['rm2'])
            else:
                pref['rm2'] = None

            if pref['rm3'] != '---':
                students.add(pref['rm3'])
            else:
                pref['rm3'] = None

        # check that the netID is in Students
        for student in students:
            query = ('SELECT * '
                     'From Students '
                     'WHERE netID = %s')
            cursor.execute(query, (student,))
            if len(cursor.fetchall()) == 0:
                return "Invalid netID: " + student + " provided"

        # check that the room is in Rooms
        for room in rooms:
            query = ('SELECT * '
                     'FROM Rooms '
                     'WHERE dorm_name = %s and room_num = %s')
            cursor.execute(query, (room[0], room[1],))
            if len(cursor.fetchall()) == 0:
                return "Invalid room: " + room[0] + "-" + room[1]


        # TODO: Make sure student isn't already in Selections

        for pref in preferences['preferences']:
            # Check to see if there already exist an entry for the netID and pref_num
            query = ('SELECT * '
                     'FROM Preferences '
                     'WHERE netID = %s and pref_num = %s')
            cursor.execute(query, (pref['netID'], pref['pref_num'],))


            # Already exist entry update the entry
            if len(cursor.fetchall()):
                update_pref = ("UPDATE Preferences "
                               "SET room = %s, dorm_name = %s, rm1 = %s, rm2 = %s, rm3 = %s "
                               "WHERE netID = %s and pref_num = %s")
                cursor.execute(update_pref, (pref['room'], pref['dorm_name'], pref['rm1'], pref['rm2'], pref['rm3'], pref['netID'], pref['pref_num'],))

            # No entry exist, insert a new tuple
            else:
                add_pref = ("INSERT INTO Preferences "
                            "(netID, pref_num, room, dorm_name, rm1, rm2, rm3) " "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(add_pref, (pref['netID'], pref['pref_num'], pref['room'], pref['dorm_name'], pref['rm1'], pref['rm2'], pref['rm3'],))

            cnx.commit()

        return "Update successful"

    # TODO
        # expect json of the form { pref_num1: n1, pref_num2: n2 }
        # run query: update Preferences set pref_num = n1 where pref_num = n2 and netID = netID and dorm_name = dorm;
    if request.method == 'PUT':
        data = request.data
        preferences = json.loads(data)

        cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
        cursor = cnx.cursor()

        # check that the netID is in Student
        query = ('SELECT * From Students WHERE netID = %s')
        cursor.execute(query, (netID,))
        if len(cursor.fetchall()) == 0:
            return "Invalid netID: " + netID + " provided"

        #check that current preference number exists
        query = ('SELECT * From Preferences WHERE netID = %s and dorm_name = %s and pref_num = %s')
        cursor.execute(query, (netID, dorm, preferences["pref_num2"]))
        if len(cursor.fetchall()) == 0:
            return "Invalid preferences number: " + str(preferences["pref_num2"]) + " provided"

        #update preferences
        #nullify 1st pref
        query = ("UPDATE Preferences set pref_num = -1 WHERE pref_num = %s and netID = %s and dorm_name = %s")
        cursor.execute(query, (preferences["pref_num1"], netID, dorm))

        #change second to 1st
        query = ("UPDATE Preferences set pref_num = %s WHERE pref_num = %s and netID = %s and dorm_name = %s")
        cursor.execute(query, (preferences["pref_num1"], preferences["pref_num2"], netID, dorm))

        #change 1st to second
        query = ("UPDATE Preferences set pref_num = %s WHERE pref_num = -1 and netID = %s and dorm_name = %s")
        cursor.execute(query, (preferences["pref_num2"], netID, dorm))

        cnx.commit()

        return "Update preferences successful"

    # TODO
        # expect json of the form { pref_num: n }
        # run query: delete from Preferences where netID = netid and dorm_name = dorm and pref_num = n;
    if request.method == 'DELETE':
        data = request.data
        preferences = json.loads(data)

        cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
        cursor = cnx.cursor()

        # check that the netID is in Student
        query = ('SELECT * From Students WHERE netID = %s')
        cursor.execute(query, (netID,))
        if len(cursor.fetchall()) == 0:
            return "Invalid netID: " + netID + " provided"

        #check that current preference number exists
        query = ('SELECT * From Preferences WHERE netID=%s and dorm_name=%s and pref_num=%s')
        cursor.execute(query, (netID, dorm, preferences["pref_num"]))
        if len(cursor.fetchall()) == 0:
            return "Invalid preferences number: " + str(preferences["pref_num"]) + " provided"

        query = ("DELETE FROM Preferences WHERE netID=%s and dorm_name=%s and pref_num=%s")
        cursor.execute(query, (netID, dorm, preferences["pref_num"]))
        cnx.commit()

        return "Delete preference successful"

@app.route('/lock/<netID>/<dorm>/')
def lock_pick(netID, dorm):

    data = request.data
    selection = json.loads(data)

    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    # Check that the roommates are in Students and not in Selections
    number_of_roommate = 0
    roommates = []
    if selection["rm1"] != "---":
        number_of_roommate += 1
        roommates.append(selection["rm1"])
    if selection["rm2"] != "---":
        number_of_roommate += 1
        roommates.append(selection["rm2"])
    if selection["rm3"] != "---":
        number_of_roommate += 1
        roommates.append(selection["rm3"])
    
    roommates.append(netID)

    for roommate in roommates:
        #Check that all roommates are valid students
        student_query = ("SELECT * FROM Students "
                         "WHERE netID = %s")
        cursor.execute(student_query, (roommate,))
        if len(cursor.fetachall()) == 0:
            return "Invalid netID: " + netID + " provided"

        #Check that no roommates have been taken yet
        selection_query = ("Select * FROM Selections "
                           "WHERE netID = %s")
        cursor.execute(selection_query, (roommate,))
        if len(cursor.fetchall()) != 0:
            return "roommate taken"

    #check if room exists and is available
    query = ('SELECT * From Rooms WHERE dorm_name = %s and room_num = %s and available = 1')
    cursor.execute(query, (dorm, selection["room"]))
    if len(cursor.fetchall()) == 0:
        return "Room not available"

    #mark room as not available
    query = ("UPDATE Rooms set available = 0 WHERE room_num = %s and dorm_name = %s")
    cursor.execute(query, (selection["room"], dorm))

    #insert all roommates and user into selection list
    for roommate in roommates:
        query = ('INSERT into Selections (netID, room_num, dorm_name) values(%s,%s,%s)')
        cursor.execute(query, (roommate, selection["room_num"], dorm))

    #delete user and roommate preferences
    for roommate in roommates:
        query = ("DELETE FROM Preferences WHERE netID=%s and dorm_name=%s")
        cursor.execute(query, (roommate, dorm))

    #set user pick locked = 1 as done
    for roommate in roommates:
        query = ("UPDATE Picks set locked = 1 WHERE netID=%s")
        cursor.execute(query, (roommate))

    cnx.commit()
    return "Great Success!"


@app.route('/signin/<netID>/')
def sign_in(netID):
    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    query = ("SELECT dorm_name FROM Students WHERE netID = %s")
    cursor.execute(query, (netID,))

    data = {}

    for i in cursor:
        data['dorm_name'] = i[0]

    return json.dumps(data)



if __name__ == '__main__':
    PORT = int(sys.argv[1].rstrip())
    app.run(host='0.0.0.0', port=PORT, debug=True)
