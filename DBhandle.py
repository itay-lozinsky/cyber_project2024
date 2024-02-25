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
        lesson_number INTEGER,
        student_username TEXT,
        teacher_username TEXT,
        verbal_feedback TEXT,
        quantitative_feedback INT
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
    else:
        return False


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
    db_info = 0
    if check == 1:
        c2.execute(f'''SELECT connected_usernames FROM Messages''')
        db_info = c2.fetchall()
    elif check == 2:
        c2.execute(f'''SELECT usernames FROM Messages''')
        db_info = c2.fetchall()
    elif check == 3:
        c1.execute(f'''SELECT student_username FROM Feedbacks''')
        db_info = c1.fetchall()
    db_info = [item for t in db_info for item in t]
    return db_info


def add_users_to_feedbacks(student_username, teacher_username):
    c1.execute(f'''INSERT INTO Feedbacks (lesson_number, student_username, teacher_username) VALUES
    (?, ?, ?) ''', (1, student_username, teacher_username))
    conn1.commit()


def list_of_students_for_teacher(teacher_username):
    c1.execute(f'''SELECT student_username FROM Feedbacks WHERE teacher_username = '{teacher_username}' ''')
    db_info = c1.fetchall()
    db_info = list(dict.fromkeys(db_info))
    return db_info


def add_feedbacks(student_username, lesson_number, verbal_feedback, quantitative_feedback):
    c1.execute(f'''UPDATE Feedbacks SET verbal_feedback = ?, quantitative_feedback = ?
        WHERE student_username = ? AND lesson_number = ?''', (verbal_feedback, quantitative_feedback, student_username, lesson_number))
    conn1.commit()


def how_much_lessons(student_username):
    c1.execute(f'''SELECT lesson_number FROM Feedbacks WHERE student_username = '{student_username}' ''')
    db_info = c1.fetchall()
    db_info = [item for t in db_info for item in t]
    return max(db_info)


def add_lesson(student_username, teacher_username):
    c1.execute(f'''INSERT INTO Feedbacks (lesson_number, student_username, teacher_username) VALUES
    (?, ?, ?) ''', (how_much_lessons(student_username)+1, student_username, teacher_username))


def last_lesson(student_username):
    c1.execute(f'''SELECT lesson_number FROM Feedbacks WHERE student_username = ? AND quantitative_feedback = ? ''', (student_username, None))
    db_info = c1.fetchall()
    db_info = [item for t in db_info for item in t]
    if len(db_info) == 1:
        return "---"
    return db_info


def check_if_first_time_connected(username):
    c1.execute(f'''SELECT * FROM Feedbacks WHERE teacher_username = '{username}'
    OR student_username = '{username}' ''')
    db_info = c1.fetchone()
    if db_info:
        return True
    else:
        return False


def feedback_per_lesson(student_username, lesson_number):
    c1.execute(f'''SELECT verbal_feedback FROM Feedbacks WHERE student_username = '{student_username}'
     AND lesson_number = '{lesson_number}' ''')
    verbal = c1.fetchone()
    c1.execute(f'''SELECT quantitative_feedback FROM Feedbacks WHERE student_username = '{student_username}'
     AND lesson_number = '{lesson_number}' ''')
    quantitative = c1.fetchone()
    if verbal[0] is None:
        return f"No Data"
    else:
        verbal = [item for t in verbal for item in t]
        quantitative = str(quantitative)
        verbal = ''.join(verbal)
        return verbal+","+quantitative[1]


def list_of_students_in_feedbacks():
    c1.execute(f'''SELECT student_username FROM Feedbacks ''')
    db_info = c1.fetchall()
    return db_info
