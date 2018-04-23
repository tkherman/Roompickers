from flask import Flask, request
import mysql.connector
import json
import os
app = Flask(__name__)

@app.route('/select/<netID>')
def query_student(netID):
    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    query = ("SELECT netID, first_name, last_name, dorm_name FROM Students WHERE netID = %s")

    cursor.execute(query, (netID,))

    data = {}

    for i in cursor:
        data['netID'] = i[0]
        data['first_name'] = i[1]
        data['last_name'] = i[2]
        data['dorm'] = i[3]

    cursor.close()
    cnx.close()

    return json.dumps(data)

@app.route('/delete/<netID>')
def delete_student(netID):
    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    command = ("DELETE FROM Students WHERE netID = %s")

    try:
        cursor.execute(command, (netID,))
    except:
        return "Deletion failed"

    cnx.commit()

    return "Deletion succeeded"

@app.route('/insert', methods = ['POST'])
def insert_student():
    netID = request.form['netID_i']
    first_name = request.form['first_name_i']
    last_name = request.form['last_name_i']
    dorm = request.form['dorm_i']

    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    insertion = ("INSERT INTO Students (netID, first_name, last_name, dorm_name) VALUES (%s, %s, %s, %s)")

    try:
        cursor.execute(insertion, (netID, first_name, last_name, dorm))
    except:
        return "Insertion failed"

    cnx.commit()

    return "Insertion succeeded"

@app.route('/update', methods = ['POST'])
def update_student():
    netID = request.form['netID_u']
    first_name = request.form['first_name_u']
    last_name = request.form['last_name_u']
    dorm = request.form['dorm_u']

    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    update = ("UPDATE Students SET first_name = %s, last_name = %s, dorm_name = %s WHERE netID = %s")

    try:
        cursor.execute(update, (first_name, last_name, dorm, netID))
    except:
        return "Update failed"

    cnx.commit()

    return "Update succeeded"

# Return available room list
@app.route('/floors/images/<netID>/<dorm_name>')
def get_floorplans(netID, dorm_name):
    path = 'data/floorplans/' + dorm_name;
    files = os.popen('ls ' + path).read();
    filenames = files.split()
    
    # dorm_name is first value in list
    filenames.insert(0, dorm_name);
    return json.dumps(filenames);

# Return available room list
@app.route('/floors/<netID>/<dorm_name>')
def get_rooms(netID, dorm_name):
    mens_dorm = ['Alumni', 'Carroll', 'Dillon', 'Duncan', 'Dunne', 'Fisher',
                 'Keenan', 'Keough', 'Knott', 'Morrisey', 'O\'Neil Family',
                 'Siegfried', 'Sorin', 'St. Edward\'s', 'Stanford', 'Zahm']
    womens_dorm = ['Badin', 'Breen-Phillips', 'Cavanaugh', 'Farley', 'Flaherty',
                   'Howard', 'Lewis', 'Lyons', 'McGlinn', 'Pasquerilla East',
                   'Pasquerilla West', 'Ryan', 'Walsh', 'Welsh Family']

    if dorm_name not in mens_dorm and dorm_name not in womens_dorm:
        return "Invalid dorm name"

    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    query = ("SELECT r.dorm_name, r.floor_num, r.room_num, r.size, r.capacity "
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
        data['rooms'].append(room)

    cursor.close()
    cnx.close()

    return json.dumps(data)

# Returns filtered room list
@app.route('/filter/<netID>/<dorm_name>/<capacity>/<floor_num>/<size_min>/<size_max>')
def filter_rooms(netID, dorm_name, capacity, floor_num, size_min, size_max): #add size filter
    mens_dorm = ['Alumni', 'Carroll', 'Dillon', 'Duncan', 'Dunne', 'Fisher',
                 'Keenan', 'Keough', 'Knott', 'Morrisey', 'O\'Neil Family',
                 'Siegfried', 'Sorin', 'St. Edward\'s', 'Stanford', 'Zahm']
    womens_dorm = ['Badin', 'Breen-Phillips', 'Cavanaugh', 'Farley', 'Flaherty',
                   'Howard', 'Lewis', 'Lyons', 'McGlinn', 'Pasquerilla East',
                   'Pasquerilla West', 'Ryan', 'Walsh', 'Welsh Family']

    if dorm_name not in mens_dorm and dorm_name not in womens_dorm:
        return "Invalid dorm name"

    cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
    cursor = cnx.cursor()

    # this query filters by floor num
    '''
    query = ("SELECT r.dorm_name, r.floor_num, r.room_num, r.size, r.capacity "
            "FROM Rooms r, Selections s "
            "WHERE r.dorm_name = %s and (r.dorm_name <> s.dorm_name or "
                "r.room_num <> s.room_num) and r.capacity = %s and r.floor_num = %s and"
                "r.size >= %s and r.size <= %s")
    cursor.execute(query, (dorm_name, capacity, floor_num, size_min, size_max))
    '''
    # this query does not filter by floot num
    query = ("SELECT r.dorm_name, r.floor_num, r.room_num, r.size, r.capacity "
             "FROM Rooms r, Selections s "
             "WHERE r.dorm_name = %s and (r.dorm_name <> s.dorm_name or "
             "r.room_num <> s.room_num) and r.capacity = %s and"
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


#    for i in cursor:
 #       data['netID'] = i[0]
  #      data['first_name'] = i[1]
   #     data['last_name'] = i[2]
    #    data['dorm'] = i[3]


    return json.dumps(data)

@app.route('/preferences/<netID>/<dorm>')
def query_preferences(netID, dorm):
    # tmp file for dummy json data
    filename = '/home/cse30246/aborowsk/tests/test_pref.json'
    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)

    return json.dumps(data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
