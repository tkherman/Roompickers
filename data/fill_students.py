import mysql.connector

config = {
    'user': 'ktong1',
    'password': 'pw',
    'host': 'localhost',
    'database': 'ktong1'
}

mens_dorm = ['Alumni', 'Carroll', 'Dillon', 'Duncan', 'Dunne', 'Fisher',
             'Keenan', 'Keough', 'Knott', 'Morrisey', 'O\'Neil Family',
             'Siegfried', 'Sorin', 'St. Edward\'s', 'Stanford', 'Zahm']
mens_names_file = 'boys_data.csv'

womens_dorm = ['Badin', 'Breen-Phillips', 'Cavanaugh', 'Farley', 'Flaherty',
               'Howard', 'Lewis', 'Lyons', 'McGlinn', 'Pasquerilla East',
               'Pasquerilla West', 'Ryan', 'Walsh', 'Welsh Family']
womens_names_file = 'girls_data.csv'

# Load data from file
mens_data = []
womens_data = []

with open(mens_names_file) as m:
    for line in m:
        mens_data.append(line.rstrip().split(','))

with open(womens_names_file) as w:
    for line in w:
        womens_data.append(line.rstrip().split(','))


cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Insert mens_data into database
dorm_i = 0
for d in mens_data:
    add_student = ("INSERT INTO Students (netID, first_name, last_name, dorm) VALUES (%s, %s, %s, %s)")
    data_student = (d[2], d[0], d[1], mens_dorm[dorm_i])
    cursor.execute(add_student, data_student)

    if dorm_i >= len(mens_dorm) - 1:
        dorm_i = 0
    else:
        dorm_i += 1

# Insert womens_data into database
dorm_i = 0
for d in womens_data:
    add_student = ("INSERT INTO Students (netID, first_name, last_name, dorm) VALUES (%s, %s, %s, %s)")
    data_student = (d[2], d[0], d[1], womens_dorm[dorm_i])
    cursor.execute(add_student, data_student)

    if dorm_i >= len(womens_dorm) - 1:
        dorm_i = 0
    else:
        dorm_i += 1

cnx.commit()
cursor.close()

cnx.close()
