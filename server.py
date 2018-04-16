from flask import Flask, request
import mysql.connector
import json
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
