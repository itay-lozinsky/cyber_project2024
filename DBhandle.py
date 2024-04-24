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
        quantitative_feedback INT,
        removed BOOL
    )
''')

c2.execute('''
    CREATE TABLE IF NOT EXISTS Messages (
        connected_usernames TEXT,
        usernames TEXT
    )
''')


def login_process(username, password):
    """
    :param username: represents the client's username
    :param password: represents the client's password
    :return: if the password is valid
    """
    c.execute(f'''SELECT * FROM Users WHERE username = '{username}' ''')
    db_info = c.fetchone()
    if db_info:
        if db_info[1] == password:
            return db_info[2]
        else:
            return "wrong password"
    return "user doesn't exist"


def remove_student(student_username):
    c1.execute(''' UPDATE Feedbacks SET removed = ? WHERE student_username = ? ''', (True, student_username))
    conn1.commit()


def if_removed(student_username):
    c1.execute(f'''SELECT * FROM Feedbacks WHERE student_username = ? AND removed = ?''', (student_username, 1))  # Use 1 for True
    db_info = c1.fetchall()
    if db_info:
        c1.execute(f'''DELETE FROM Feedbacks WHERE student_username = ? AND removed = ?''', (student_username, 1))
        conn1.commit()
        return db_info
    else:
        return ["False"]


def registration_process(username, password, user_type):
    """
    :param username: represents the client's username
    :param password: represents the client's password
    :param user_type: represents the client's user type
    :return: it creates the user and returns the user type (student, teacher, friend) if it's valid
    """
    c.execute(f'''SELECT * FROM Users WHERE username = '{username}' ''')
    db_info = c.fetchone()
    if db_info:
        return "user already exists"
    else:
        c.execute(f'''INSERT INTO Users VALUES ('{username}','{password}','{user_type}')''')
        conn.commit()
        return user_type


def list_of_students(check):
    """
    :param check: 1 for getting the list of the students who chose to hide their account while disconnected.
    2 for getting the list of all the students who joined the system. 3 for getting the list of all the students
    who already connected with their teacher
    :return: one of these lists
    """
    db_info = 0
    if check == 1:
        c2.execute(f'''SELECT connected_usernames FROM Messages''')
        db_info = c2.fetchall()
    elif check == 2:
        c2.execute(f'''SELECT usernames FROM Messages''')
        db_info = c2.fetchall()
    elif check == 3:
        c1.execute(f'''SELECT student_username FROM Feedbacks WHERE removed = '{0}' ''')
        db_info = c1.fetchall()
    db_info = [item for t in db_info for item in t]
    return db_info


def add_student(yes_or_no, student_username):
    """
    :param yes_or_no: the button the student clicked on
    :param student_username: represents the username of the student
    :return: it adds the student username to the messages chart
    """
    if yes_or_no == "YES":
        c2.execute(f'''INSERT INTO Messages (connected_usernames) VALUES ('{student_username}') ''')
    else:
        c2.execute(f'''INSERT INTO Messages (usernames) VALUES ('{student_username}') ''')
    conn2.commit()


def add_users_to_feedbacks(student_username, teacher_username):
    """
    :param student_username: represents the username of the student
    :param teacher_username: represents the username of the teacher
    :return: it adds a student who connected with his teacher to the feedbacks chart
    """
    c1.execute(f'''INSERT INTO Feedbacks (lesson_number, student_username, teacher_username, verbal_feedback, quantitative_feedback, removed) VALUES
    (?, ?, ?, ?, ?, ?) ''', (1, student_username, teacher_username, "None", "None", False))
    conn1.commit()


def list_of_students_per_teacher(teacher_username):
    """
    :param teacher_username: represents the username of the teacher
    :return: the list of all the students who connected to the teacher
    """
    c1.execute(f'''SELECT student_username FROM Feedbacks WHERE teacher_username = '{teacher_username}' AND removed = '{0}' ''')
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
    return str(max(db_info))


def add_lesson(student_username, teacher_username):
    c1.execute(f'''INSERT INTO Feedbacks (lesson_number, student_username, teacher_username, verbal_feedback, quantitative_feedback, removed) VALUES
    (?, ?, ?, ?, ?, ?) ''', (int(how_much_lessons(student_username))+1, student_username, teacher_username, "None", "None", False))
    conn1.commit()


def last_lesson(student_username):
    c1.execute(f'''SELECT lesson_number FROM Feedbacks WHERE student_username = ? AND verbal_feedback = ? ''', (student_username, "None"))
    db_info = c1.fetchall()
    db_info = [item for t in db_info for item in t]
    if db_info:
        if db_info[0] == 1:
            return "---"
        return str(min(db_info)-1)
    else:
        return str(how_much_lessons(student_username))


def step1(username):
    c2.execute(f'''SELECT * FROM Messages WHERE connected_usernames = '{username}'
    OR usernames = '{username}' ''')
    db_info = c2.fetchone()
    if db_info:
        return "1"
    else:
        return "0"


def step2(username):
    c1.execute(f'''SELECT * FROM Feedbacks WHERE teacher_username = '{username}'
    OR student_username = '{username}' AND removed = '{0}' ''')
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
    c1.execute(f'''SELECT teacher_username FROM Feedbacks WHERE student_username = '{student_username}' ''')
    teacher_username_tuple = c1.fetchone()
    teacher_username = teacher_username_tuple[0]
    if quantitative[0] == "None":
        return f"Teacher {teacher_username[9:]} didn't update feedback for lesson number {lesson_number} yet \n"
    else:
        verbal = [item for t in verbal for item in t]
        verbal = ''.join(verbal)
        quantitative = str(quantitative)
        return f"Teacher {teacher_username[9:]}'s feedback for lesson number {lesson_number}: {verbal}, {quantitative[1]} \n"

def friends_list():
    c.execute(f'''SELECT username FROM Users WHERE type == "Friend" ''')
    db_info = c.fetchall()
    db_info = [item for t in db_info for item in t]
    return db_info
