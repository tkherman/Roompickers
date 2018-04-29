import mysql.connector
import datetime

cnx = mysql.connector.connect(user='ktong1', password='pw', host='localhost', database='ktong1')
cursor = cnx.cursor()

def select_room(dorm_name, pick, netID):
    # Query the preferences for the student with netID
    pref_query = ("SELECT * FROM Preferences "
                  "WHERE netID = %s and dorm_name = %s "
                  "ORDER BY pref_num"
    cursor.execute(pref_query, (netID, dorm_name,))

    prefs = cursor.fetachall()

    # Go through the preferences, and lock in the first preference that is available
    for (netID, pref_num, room, dorm_name, rm1, rm2, rm3) in prefs:
        available_query = ("SELECT available FROM Rooms "
                           "WHERE dorm_name = %s and room = %s")
        cursor.execute(available_query, (dorm_name, room,))

        # continue to next preference if the room is not available
        if cursor.fetchall()[0][0] == 0:
            continue

        # Check that the roommates are in Students and not in Selections
        number_of_roommate = 0
        roommates = []
        if rm1 != "---":
            number_of_roommate += 1
            roommates.append[rm1]
        if rm2 != "---":
            number_of_roommate += 1
            roommates.append[rm2]
        if rm3 != "---":
            number_of_roommate += 1
            roommates.append[rm3]

        # Check that each roommate is a student and have not been
        # locked into a room
        all_in = True
        for roommate in roommates:
            student_query = ("SELECT * FROM Students "
                             "WHERE netID = %s")
            cursor.execute(student_query, (roommate,))
            if len(cursor.fetachall()) == 0:
                all_in = False
                break
            selection_query = ("Select * FROM Selections "
                               "WHERE netID = %s")
            cursor.execute(selection_query, (roommate,))
            if len(cursor.fetchall()) != 0:
                all_in = False
                break

        if not all_in:
            continue

        # Lock in the room
        lock_in = ("INSERT INTO Selections VALUES (%s, %s, %s)")
        cursor.execute(lock_in, (netID, room, dorm_name,))
        for roommate in roommates:
            cursor.execute(lock_in, (roommate, room, dorm_name,))

        # Mark room as unavailable
        update_avail = ("UPDATE Rooms SET available = 0 WHERE dorm_name = %s and room_num = %s")
        cursor.execute(update_avail, (dorm_name, room,))

        # Take roommates and student out of Picks and Preferences
        delete_picks = ("DELETE FROM PICKS WHERE netID = %s")
        delete_prefs = ("DELETE FROM Preferences WHERE netID = %s")
        cursor.execute(delete_picks, (netID,))
        cursor.execute(delete_prefs, (netID,))
        for roommate in rorommates:
            cursor.execute(delete_picks, (roommate,))
            cursor.execute(delete_prefs, (roommate,))

    cnx.commit()

    # TODO: WHAT IF NO PREFERENCES ARE AVAILABLE



def main():
    # Run through Picks to see if, for any students, the end time has passed and
    # they haven't locked in.
    pick_query = ("SELECT dorm_name, pick, netID, end FROM Picks "
                  "WHERE locked = 0"
    cursor.execute(pick_query)

    picks = cursor.fetchall()
    for (dorm_name, pick, netID, end) in picks:
        # Load end as datetime object
        end_time = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        # Auto pick for the student
        if end_time > datetime.now():
            select_room(dorm_name, pick, netID)

if __name__ == "__main__":
    main()
