import csv
import os
import sqlite3

# Resolve the resources folder relative to this file, so paths work
# no matter what directory the script is run from.
_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'resources')

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users(os.path.join(_RESOURCES_DIR, 'users.csv'))
    load_and_clean_call_logs(os.path.join(_RESOURCES_DIR, 'callLogs.csv'))
    write_user_analytics(os.path.join(_RESOURCES_DIR, 'userAnalytics.csv'))
    write_ordered_calls(os.path.join(_RESOURCES_DIR, 'orderedCalls.csv'))

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    # select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    #print("TODO: load_users")
    with open(file_path, 'r', newline='') as userFile: # opens the file path to read
        # reads the file one row at a time
        reader = csv.reader(userFile)

        # we're looking at each row as a list of values
        for row in reader:
            # removes any unnecessary characters from the records 
            row = [value.strip() for value in row]
            # checks if there's a value and skips the first row becasue they're column labels
            if row and row[0].lower() == "firstname": 
                continue
            # skips rows that doesn't have at exectly two column values
            if len(row) != 2:
                continue
            # skips rows with empty values
            if not all(row):
                continue
            # inserts the values in users.csv into users table
            cursor.execute('''INSERT INTO users (firstname, lastname) VALUES (?, ?)''', row)
    conn.commit() # updates the database and users table with changes


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    #print("TODO: load_call_logs")
    with open(file_path, 'r', newline='') as callLogs:
        # reads the file one row at a time 
        reader = csv.reader(callLogs)

        # looking at each row as a list of values
        for row in reader:
            # removes any unnecessary characters from the values:
            row = [value.strip() for value in row]
            # checks if there is a value and skips the first row
            if row and row[0].lower() == "phonenumber":
                continue
            # skips the row if it doesn't have exactly five column values
            if len(row) != 5:
                continue
            # skips rows with empty values
            if not all(row):
                continue
            ### checks if the userID(FK) in callLogs table maps to a userID in the users table
            # check_userId = "SELECT 1 FROM users WHERE userId = ?"
            # fk_value = row[-1]
            # cursor.execute(check_userId, (fk_value, ))
            # isExist = cursor.fetchone()
            # if isExist is None:
            #    continue

            # inserts the values of each row into the tables as a records
            cursor.execute('''INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId) VALUES (?, ?, ?, ?, ?)''', row)
    conn.commit() #updates the database and callLogs tables with changes


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    #print("TODO: write_user_analytics")
    with open(csv_file_path, 'w') as testAnalytics:
            # returns the results of userId, avgDuration, and numCalls
            cursor.execute("SELECT userId, AVG(endTime - startTime), COUNT(*) FROM callLogs GROUP BY userId ORDER BY userId")

            #includes the header each time the function to avoid truncating unwanted things
            testAnalytics.write("userId,avgDuration,numCalls\n")
            # loops through the results of the query
            for row in cursor:
                row = ",".join(str(value) for value in row) # combines each value in a row into x,y,z, also coverting to string
                testAnalytics.write(row + "\n") # writing the string row to the csv file



# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):
    #print("TODO: write_ordered_calls")
    with open(csv_file_path, 'w') as orderedCalls:
        # includes the header of the csv file each time the file is written into
        orderedCalls.write("callId,phoneNumber,startTime,endTime,direction,userId")
        # returns all records of callLogs but is ordered by userId and startTime
        cursor.execute('''SELECT * FROM callLogs ORDER BY userId ASC, startTime ASC''')

        # loops through the results of the query
        for row in cursor:
            row = ",".join(str(value) for value in row) # converts each value into a string and joins them with a comma
            orderedCalls.write(row + "\n")



# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()