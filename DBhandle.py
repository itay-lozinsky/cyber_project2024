import sqlite3


class Database:
    """
    A base class for managing SQLite databases.
    """

    def __init__(self, db_name):
        """
        Initialize the Database object with the given database name.

        :param db_name: The name of the SQLite database.
        """
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()


class UsersDatabase(Database):
    """
    A class for managing the Users table in an SQLite database.
    Inherits from the Database class.
    """

    def __init__(self, db_name):
        """
        Initialize the UsersDatabase object with the given database name.
        Create the Users table if it doesn't exist.

        :param db_name: The name of the SQLite database.
        """
        super().__init__(db_name)
        self.create_table()

    def create_table(self):
        """
        Create the Users table if it doesn't exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                username TEXT,
                password TEXT,
                type TEXT
            )
        ''')
        self.conn.commit()

    def registration_process(self, username, password, user_type):
        """
        Register a new user to the system.

        :param username: The username of the new user trying to register.
        :param password: The password of the new user trying to register.
        :param user_type: The type of the new user trying to register.
        :return: The user type if registration is successful, otherwise an error message.
        """
        self.cursor.execute(f'''SELECT * FROM Users WHERE username = '{username}' ''')
        db_info = self.cursor.fetchone()
        if db_info:
            return "user already exists"
        else:
            self.cursor.execute(f'''INSERT INTO Users VALUES (?, ?, ?)''', (username, password, user_type))
            self.conn.commit()
            return user_type

    def login_process(self, username, password):
        """
        Check login credentials and return user type if successful.

        :param username: The username of the user trying to log in.
        :param password: The password of the user trying to log in.
        :return: The user type if login is successful, otherwise an error message.
        """
        self.cursor.execute(f'''SELECT * FROM Users WHERE username = '{username}' ''')
        db_info = self.cursor.fetchone()
        if db_info:
            if db_info[1] == password:
                return db_info[2]  # Return user type if password is correct
            else:
                return "wrong password"
        return "user doesn't exist"

    def friends_list(self):
        """
        :return: A list of all friend usernames, using the "Users" table.
        """
        self.cursor.execute(f'''SELECT username FROM Users WHERE type == "Friend" ''')
        db_info = self.cursor.fetchall()
        db_info = [item for t in db_info for item in t]
        return db_info

    def list_of_students(self, check):
        """
        :param check: 1 for getting the list of students who chose to hide their account while disconnected (Chose YES),
                      2 for getting the list of all students who joined the system (Chose NO),
                      3 for getting the list of all students who already connected with their teacher
                      In the server, list 1 & list 2 will be united,
                      and the students shown in list 3 will be removed from the united list.
        :return: A list of usernames based on the specified check.
        Note: Although this func retrieves data from number of tables,
         it's under the "UsersDatabase" class, for convenience.
        """
        try:
            db_info = []
            if check == 1:
                self.cursor.execute('''SELECT connected_usernames FROM Messages''')
                db_info = self.cursor.fetchall()
            elif check == 2:
                self.cursor.execute('''SELECT usernames FROM Messages''')
                db_info = self.cursor.fetchall()
            elif check == 3:
                self.cursor.execute('''SELECT student_username FROM Feedbacks WHERE removed = ?''', ('0',))
                db_info = self.cursor.fetchall()
            db_info = [item for t in db_info for item in t]
            return db_info
        except sqlite3.Error as e:
            print(f"Error retrieving list of students: {e}")
            return []


class WaitingStudentsDatabase(Database):
    """
    A class for managing the Users table in an SQLite database.
    Inherits from the Database class.
    """
    def __init__(self, db_name):
        """
        Initialize the UsersDatabase object with the given database name.
        Create the Users table if it doesn't exist.

        :param db_name: The name of the SQLite database.
        """
        super().__init__(db_name)
        self.create_table()

    def create_table(self):
        """
        Create the Feedbacks table if it doesn't exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Waiting_Students (
                YES_username TEXT,
                NO_username TEXT
            )
        ''')
        self.conn.commit()

    def add_student(self, yes_or_no, student_username):
        """
        Add a student to the Waiting_Students table based on their choice.

        :param yes_or_no: The button the student clicked on (either "YES" or "NO").
        :param student_username: The username of the student being connected by their teacher.
        """
        try:
            if yes_or_no == "YES":
                self.cursor.execute("INSERT INTO Waiting_Students (YES_username) VALUES (?)", (student_username,))
            elif yes_or_no == "NO":
                self.cursor.execute("INSERT INTO Waiting_Students (NO_username) VALUES (?)", (student_username,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding student to Messages: {e}")

    def stage_number1(self, student_username):
        """
        Checks if the student is in the Messages table, indicating stage 1
         (Means that he already chose YES or NO).
        :param student_username: The username of the student being checked.
        :return: "1" if the student is found, "0" otherwise.
        """
        self.cursor.execute(f'''SELECT * FROM Waiting_Students WHERE YES_username = '{student_username}'
        OR usernames = '{student_username}' ''')
        db_info = self.cursor.fetchone()
        if db_info:
            return "1"
        else:
            return "0"


class FeedbacksDatabase(Database):
    """
    A class for managing the Users table in an SQLite database.
    Inherits from the Database class.
    """
    def __init__(self, db_name):
        """
        Initialize the FeedbackDatabase object with the given database name.
        Create the Users table if it doesn't exist.

        :param db_name: The name of the SQLite database.
       """
        super().__init__(db_name)
        self.create_table()

    def create_table(self):
        """
        Create the Feedbacks table if it doesn't exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Feedbacks (
                lesson_number INTEGER,
                student_username TEXT,
                teacher_username TEXT,
                verbal_feedback TEXT,
                quantitative_feedback INT,
                removed BOOL
            )
        ''')
        self.conn.commit()

    def stage_number2(self, username):
        """
        Checks if the student is in the Feedbacks table, indicating stage 2.
        Also checks if the teacher has connected at least one student to the system by being in the Feedbacks table.

        :param username: The username of the user being checked.
        :return: True if the user is found, False otherwise.
        """
        self.cursor.execute(f'''SELECT * FROM Feedbacks 
                                WHERE (teacher_username = ? OR student_username = ?) 
                                AND removed = ?''', (username, username, '0'))
        db_info = self.cursor.fetchone()
        if db_info:
            return "True"
        else:
            return "False"

    def add_users_to_feedbacks(self, student_username, teacher_username):
        """
        Adds a new entry for the specified student and teacher in the Feedbacks table.
        That means, both connection stages of the student are completed.

        Note: Since this marks the student's connection to the system by the teacher,
        the first lesson is created automatically - there's no need for the teacher to click "Add Lesson".

        :param student_username: The username of the student.
        :param teacher_username: The username of the teacher.
        """
        self.cursor.execute(
            '''INSERT INTO Feedbacks (lesson_number, student_username, teacher_username, 
            verbal_feedback, quantitative_feedback, removed) 
            VALUES (?, ?, ?, ?, ?, ?) ''', (1, student_username, teacher_username, "None", "None", False))
        self.conn.commit()

    def list_of_students_per_teacher(self, teacher_username):
        """
        Retrieves a list of students connected to a specific teacher.
        It's used so the teacher can see all of their students.

        :param teacher_username: The username of the teacher.
        :return: A list of student usernames.
        """
        self.cursor.execute(
            '''SELECT student_username FROM Feedbacks WHERE teacher_username = ? AND removed = ?''',
            (teacher_username, '0'))
        db_info = self.cursor.fetchall()
        db_info = [item for t in db_info for item in t]
        db_info = list(dict.fromkeys(db_info))
        return db_info

    def how_much_lessons(self, student_username):
        """
        Calculates the maximum lesson number for a student.
        Used for the teacher and the student to see the last lesson number added.

        :param student_username: The username of the student.
        :return: The maximum lesson number as a string.
        """
        self.cursor.execute('''SELECT MAX(lesson_number) FROM Feedbacks WHERE student_username = ?''',
                            (student_username,))
        max_lesson = self.cursor.fetchone()[0]
        return str(max_lesson) if max_lesson is not None else "0"

    def add_lesson(self, student_username, teacher_username):
        """
        Adds a new lesson for a student, incrementing the lesson number based on existing lessons.

        :param student_username: The username of the student.
        :param teacher_username: The username of the teacher.
        """
        current_lesson = self.how_much_lessons(student_username)
        if current_lesson is not None:
            lesson_number = int(current_lesson) + 1
            self.cursor.execute('''INSERT INTO Feedbacks (lesson_number, student_username, teacher_username,
                                   verbal_feedback, quantitative_feedback, removed) VALUES (?, ?, ?, ?, ?, ?)''',
                                (lesson_number, student_username, teacher_username, "None", "None", False))
            self.conn.commit()
        else:
            print("Error: Could not determine the current lesson number.")

    def last_entered_lesson(self, student_username):
        """
        Retrieves the last entered lesson for a student based on feedback data.

        :param student_username: The username of the student.
        :return: A string indicating the last entered lesson or feedback status.
        """
        self.cursor.execute(
            '''SELECT lesson_number FROM Feedbacks WHERE student_username = ? AND verbal_feedback = ?''',
            (student_username, "None"))
        db_info = self.cursor.fetchall()
        db_info = [item for t in db_info for item in t]
        if db_info:
            # Determine the last entered lesson
            last_lesson_number = min(db_info) - 1
            if last_lesson_number > 0:
                return f"The last entered lesson is: {last_lesson_number}"
            else:
                return "No entered feedback yet"
        else:
            return "Feedback has been entered in all lessons"

    def add_feedback(self, student_username, lesson_number, verbal_feedback, quantitative_feedback):
        """
        Adds or updates the feedback data for a specific student and lesson.

        :param student_username: The username of the student.
        :param lesson_number: The lesson number.
        :param verbal_feedback: The verbal feedback.
        :param quantitative_feedback: The quantitative feedback.
        """
        self.cursor.execute('''UPDATE Feedbacks SET verbal_feedback = ?, quantitative_feedback = ?
            WHERE student_username = ? AND lesson_number = ?''',
                            (verbal_feedback, quantitative_feedback, student_username, lesson_number))
        self.conn.commit()

    def feedback_per_lesson(self, student_username, lesson_number):
        """
        Retrieves the feedback for a specific lesson of a student.

        :param student_username: The username of the student.
        :param lesson_number: The lesson number.
        :return: A string containing the feedback data (includes verbal & quantitative feedback,
                 lesson number, and teacher username).
        """
        try:
            # Retrieve verbal feedback
            self.cursor.execute('''SELECT verbal_feedback FROM Feedbacks 
                                    WHERE student_username = ? AND lesson_number = ?''',
                                (student_username, lesson_number))
            verbal_feedback = self.cursor.fetchone()
            verbal_feedback = verbal_feedback[0]

            # Retrieve quantitative feedback
            self.cursor.execute('''SELECT quantitative_feedback FROM Feedbacks 
                                    WHERE student_username = ? AND lesson_number = ?''',
                                (student_username, lesson_number))
            quantitative_feedback = self.cursor.fetchone()
            quantitative_feedback = quantitative_feedback[0]

            # Retrieve teacher username
            self.cursor.execute('''SELECT teacher_username FROM Feedbacks 
                                    WHERE student_username = ?''',
                                (student_username,))
            teacher_username_tuple = self.cursor.fetchone()
            teacher_username = teacher_username_tuple[0]

            if quantitative_feedback == "None":
                return f"Teacher {teacher_username[9:]} didn't update feedback for lesson number {lesson_number} yet."
            else:
                verbal_feedback = ''.join(verbal_feedback)
                quantitative_feedback = str(quantitative_feedback)
                return f"Teacher {teacher_username[9:]}'s feedback for lesson number {lesson_number}: " \
                       f"{verbal_feedback},{quantitative_feedback[1]}."

        except sqlite3.Error as e:
            print(f"Error retrieving feedback: {e}")
            return "Error retrieving feedback."

    def remove_student(self, student_username):
        """
        Marks a student as removed by updating the 'removed' status to True in the Feedbacks table.

        :param student_username: The username of the student to be marked as removed.
        """
        self.cursor.execute('''UPDATE Feedbacks SET removed = ? WHERE student_username = ?''',
                            (True, student_username))
        self.conn.commit()

    def if_removed(self, student_username):
        """
        Checks if a student has been marked as removed in the Feedbacks table and removes them if found.

        :param student_username: The username of the student to check for removal.
        :return: If the student is marked as removed, their information is returned;
         Otherwise, ["False"] is returned to indicate that the student is not marked as removed.
        """
        self.cursor.execute('''SELECT * FROM Feedbacks WHERE student_username = ? AND removed = ?''',
                            (student_username, True))
        db_info = self.cursor.fetchall()
        if db_info:
            self.cursor.execute('''DELETE FROM Feedbacks WHERE student_username = ? AND removed = ?''',
                                (student_username, True))
            self.conn.commit()

        return db_info if db_info else ["False"]
