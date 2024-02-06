import sqlite3

conn = sqlite3.connect('Users.db', check_same_thread=False)  # creates a table with the client's details
c = conn.cursor()

conn1 = sqlite3.connect('Feedbacks.db', check_same_thread=False)  # creates a table with the teacher's feedbacks
c1 = conn1.cursor()

conn2 = sqlite3.connect('Messages.db', check_same_thread=False)  # creates a reference table
c2 = conn2.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        username TEXT,
        password TEXT,
        type TEXT
    )
''')

c1.execute('''
    CREATE TABLE IF NOT EXISTS Feedbacks (
        student_usernames TEXT,
        teacher_usernames TEXT,
        verbal_feedbacks TEXT,
        quantitative_feedbacks INT
    )
''')

c2.execute('''
    CREATE TABLE IF NOT EXISTS Messages (
        connected_usernames TEXT,
        usernames TEXT
    )
''')


def check_password(username, password):
    """
    :param username: represents the client's username
    :param password: represents the client's password
    :return: if the password is valid
    """
    c.execute(f'''SELECT * FROM Users WHERE username = '{username}' ''')
    db_info = c.fetchone()
    if db_info:
        if db_info[0] == username and db_info[1] == password:
            return db_info[2]
        else:
            return "FALSE"
    return "user doesnt exist"


def create_user(username, password, user_type):
    """
    :param username: represents the client's username
    :param password: represents the client's password
    :param user_type: represents the client's user type
    :return: it creates the user and returns the user type (student, teacher, friend)
    """
    c.execute(f'''SELECT * FROM Users WHERE username = '{username}' ''')
    db_info = c.fetchone()
    if db_info:
        return "user is already exists"
    else:
        c.execute(f'''INSERT INTO Users VALUES ('{username}','{password}','{user_type}')''')
        conn.commit()
        return user_type


def is_joined(student_username):
    """
    :param student_username: represents the student's username
    :return: checks if it's the first time the student connected to the system
    """
    c2.execute(f'''SELECT * FROM Messages WHERE connected_usernames = '{student_username}'
    OR usernames = '{student_username}' ''')
    db_info = c2.fetchone()
    if db_info:
        return True


def add_student(yes_or_no, username):
    if yes_or_no == "YES":
        c2.execute(f'''INSERT INTO Messages (connected_usernames) VALUES ('{username}') ''')
    else:
        c2.execute(f'''INSERT INTO Messages (usernames) VALUES ('{username}') ''')
    conn2.commit()


def list_of_students(check):
    """
    :param check: 1 for getting the list of the students who chose to hide their account while disconnected.
    2 for getting the list of all the student who joined the system
    :return:
    """
    if check == 1:
        c2.execute(f'''SELECT connected_usernames FROM Messages''')
    else:
        c2.execute(f'''SELECT usernames FROM Messages''')
    return c2.fetchall()
