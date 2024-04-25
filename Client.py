from tkinter import messagebox
from Objects import Enum
import threading
import Windows
import socket
import pickle
import File


# Create a socket for client-server communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
Creates a TCP socket for connecting to a server. AF_INET specifies the address family as IPv4, 
and SOCK_STREAM specifies the socket type as a stream socket for TCP.
"""
client_socket.connect(('localhost', 4444))
"""
Connects the client socket to the server running on localhost (127.0.0.1) at port 4444. 
Replace 'localhost' with the actual IP address or hostname of the server if it's on a different machine.
"""


def is_fit_password(password):
    """
    Checks if the password meets the necessary security conditions for "strong password"
    and returns True or False accordingly.
    :param password: The password entered by the user during registration/connection the system.
    :return: bool: True if the password meets the conditions, False otherwise.
    """
    # Condition 1: At least 3 uppercase letters
    uppercase_count = sum(1 for char in password if char.isupper())
    if uppercase_count < 3:
        return False

    # Condition 2: At least 3 lowercase letters
    lowercase_count = sum(1 for char in password if char.islower())
    if lowercase_count < 3:
        return False

    # Condition 3: At least 2 digits
    digit_count = sum(1 for digit in password if digit.isdigit())
    if digit_count < 2:
        return False

    # Condition 4: At least one special character from &/!/#/@
    special_characters = ["&", "!", "#", "@"]
    if not any(char in special_characters for char in password):
        return False

    # Condition 5: At least 12 characters
    if len(password) < 12:
        return False

    # All conditions met
    return True


def registration_check(username_entry, password_entry, type_entry, self_para):
    """
    :param username_entry: Entry widget for username.
    :param password_entry: Entry widget for password.
    :param type_entry: Entry widget for user type.
    :param self_para: The root object of Tkinter library.
    Checks if the username and password meet the required conditions for registration.
    If valid, send registration data to the server. If not, informs the user through dedicated message boxes.
    The server returns the user type if everything is okay,
    and "user already exists" if the username is already taken by another user
    (In that case, the user will be informed as well).
    Finally, if everything is okay, the user is navigated to the "division_between_clients" function.
    """

    username = username_entry.get()
    password = password_entry.get()
    user_type = type_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "You need to enter your details.")
    elif user_type == "":
        messagebox.showerror("Error", "You need to choose your user type.")
    elif len(username) < 12 or username[9] != "_" or not username[0:8].isdigit():
        messagebox.showerror("Error", "Invalid username format. Please use the correct format.")
    elif not is_fit_password(password):
        messagebox.showerror("Error", "Your password is not strong enough. Please follow the conditions.")

    else:
        client_socket.send(f"{Enum.REGISTRATION}*{username}*{password}*{user_type}".encode())
        answer = client_socket.recv(1024).decode()

        if answer == "user already exists":
            messagebox.showerror("Error", "The user already exists.")
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")
        elif answer in ["Student", "Teacher", "Friend"]:
            messagebox.showinfo("Success", "You have successfully registered.")
            division_between_users(user_type, username, self_para)
        else:
            messagebox.showerror("Registration Error", "Failed to connect to the server. Please try again later.")


def login_check(username_entry, password_entry, self_para):
    """
    :param username_entry: Entry widget for username.
    :param password_entry: Entry widget for password.
    :param self_para: The root object of Tkinter library.
    Sends the login data to the server.
    The server returns the user type if everything is okay,
    "user doesn't exist" if the username doesn't exist in the system,
    and "wrong password" if the password doesn't match the username.
    In all these cases, the user will be informed through dedicated message boxes.
    Finally, if everything is okay, the user is navigated to the "division_between_clients" function.
    Note: I will not write anymore that the functions connect to the server, since it is self-explanatory.
    """

    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "You need to enter your details.")

    else:
        client_socket.send(f"{Enum.LOGINING}*{username}*{password}".encode())
        answer = client_socket.recv(1024).decode()

        if answer == "user doesn't exist":
            messagebox.showerror("False details", "This user does not exist.")
            username_entry.delete(0, "end")
        elif answer == "wrong password":
            messagebox.showerror("False Details", "This password is wrong. Please try again.")
            password_entry.delete(0, "end")
        elif answer in ["Student", "Teacher", "Friend"]:
            messagebox.showinfo("Success", "You have successfully logged in.")
            division_between_users(answer, username, self_para)
        else:
            messagebox.showerror("Connection Error", "Failed to connect to the server. Please try again later.")


def division_between_users(user_type, username, self_para):
    """
    :param user_type: The user type chosen by the user during registration/connection the system.
    :param username: The user type entered by the user during registration/connection the system.
    :param self_para: The root object of Tkinter library.
    :return: Routes each user to their path based on their user type and on other data,
     according to the following division:

     For Student users:
    - If passed stage 2 in registration, opens "StudentFeedbacksFrame".
    - If not passed stage 2 but passed stage 1, checks if they have been removed since the last time they logged in:
        - If removed, opens "JoiningStudentFrame" with option 2 (connection already established).
        - If not removed, opens "JoiningStudentFrame" with option 1 (waiting to connect with a teacher).
    - If not passed stage 1, opens JoiningStudentFrame with option 0 (did not choose YES or NO yet).

    For Teacher users:
    - If passed stage 2 in registration, opens "TeacherFeedbacksFrame".
    - If not passed stage 2, opens "TeacherOptionsFrame".

    For Friend users:
    - Opens "FriendsGetTheFeedbackFrame" directly.
    """
    if user_type == "Student":
        if passed_stage_number2(username) == "True":
            handle_student_connection_status(self_para, username, 0)  # option0-removed while being disconnected from the system
            Windows.StudentFeedbacksFrame(self_para, username, 0)  # option0-entered the frame from the division func.
        else:
            if passed_stage_number1(username) == "1":
                if handle_student_connection_status(self_para, username, 0) != ["False"]:  # option0-removed while being disconnected from the system
                    Windows.JoiningStudentFrame(self_para, username, 2)  # option2-connection already established
                else:
                    Windows.JoiningStudentFrame(self_para, username, 1)  # option1-waiting to connect with a teacher
            else:
                Windows.JoiningStudentFrame(self_para, username, 0)  # option0-did not choose YES or NO yet
    if user_type == "Teacher":
        if passed_stage_number2(username) == "True":
            Windows.TeacherFeedbacksFrame(self_para, username)
        else:
            Windows.TeacherOptionsFrame(self_para, username)
    if user_type == "Friend":
        Windows.FriendsGetTheFeedbackFrame(self_para, username)


def passed_stage_number1(student_username):
    """
    An overview of the two stages involved in connecting to the system (for students):
    in the first stage, the student is required to choose "YES" or "NO"
    (further explanation available in the project book).
    In the second stage, the student waits for a connection from their teacher.
    Once connected by the teacher, both connection stages are completed.
    :return: returns "1" if the student already chose "YES" or "NO" (indicating completion of the first stage)
     and "0" if not.
    """
    client_socket.send(f"{Enum.STAGE1}*{student_username}".encode())
    return client_socket.recv(1024).decode()


def passed_stage_number2(username):
    """
    Provides an overview as given in the stage1 function.
    :return: returns "True" if the student has already been connected by the teacher, and "False" if it didn't.
    Note: The function is also used to check if the *teacher* has connected at least one student to the system.
    """
    client_socket.send(f"{Enum.STAGE2}*{username}".encode())
    return client_socket.recv(1024).decode()


def list_of_students():
    """
    :return: the list of all the students currently ready to connect,
     including: the connected students who chose "YES" and all the students who chose "NO".
     NoteI: of course, this list does not include students who have already connected with their teacher.
     NoteII: the list includes removed students.
    """
    client_socket.send(f"{Enum.STUDENT_LIST}".encode())
    return pickle.loads(client_socket.recv(1024))


def add_clients_to_yes_or_no_table(self_para, answer, student_username):
    """
    :param self_para: The root object of Tkinter library.
    :param answer: The choice of the students - True for "YES" and False for "NO". This chose is unchangeable.
    :param student_username: The username of the student.
    Adds the student to the yes_or_no table, so that they can be included in the students list.
    Also navigates the student to the "JoiningStudentFrame" after the choice is made.
    """
    warning = messagebox.askyesno("A Warning", "Are you sure? You can only choose one time")
    if warning:
        if answer:
            messagebox.showinfo("Success", "You successfully chose YES!")
            client_socket.send(f"{Enum.YES}*{student_username}".encode())
        else:
            messagebox.showinfo("Success", "You successfully chose NO!")
            client_socket.send(f"{Enum.NO}*{student_username}".encode())
        Windows.JoiningStudentFrame(self_para, student_username, 1)


def get_the_next_frame(self_para, student_username):
    """
    :param self_para: The root object of Tkinter library.
    :param student_username: The username of the student who waits for connection from the teacher.
    It's activated as a thread. Navigates the student to the "StudentFeedbacksFrame" when the teacher connects them.
    """
    template = ""
    text_message = "The Next Frame"
    while template != text_message:
        template = client_socket.recv(1024).decode()
    Windows.StudentFeedbacksFrame(self_para, student_username, 0)  # option0-entered the frame from the division func.


def teacher_connecting_student(self_para, teacher_username, student_username_entry, listbox):
    """
    :param self_para: The root object of Tkinter library.
    :param teacher_username: The username of the teacher who connects the student.
    :param student_username_entry: The selected student's username entry.
    :param listbox: The listbox widget containing student usernames.
    Checks if a student username is selected from the listbox and if it's still available.
    If the selection is valid, it sends a message to the chosen student to proceed to the next frame
    and navigates the teacher to the "TeacherFeedbacksFrame".
    """
    if not student_username_entry:
        messagebox.showerror("Error", "You need to choose a student")
    student_username = listbox.get(student_username_entry[0])
    if student_username not in list_of_students():
        messagebox.showerror("Error", "This student is not on the options anymore. Please choose"
                                      "another student or try again later.")
    else:
        client_socket.send(f"{Enum.THE_NEXT_FRAME}*{student_username}*{teacher_username}".encode())
        Windows.TeacherFeedbacksFrame(self_para, teacher_username)


def list_of_students_per_teacher(teacher_username):
    """
    :param teacher_username: The username of the teacher who connected at least one student.
    :return: Returns list of students this teacher has connected.
    """
    client_socket.send(f"{Enum.LIST_STUDENTS_PER_TEACHER}*{teacher_username}".encode())
    answer = pickle.loads(client_socket.recv(1024))
    #answer = [item for t in answer for item in t]
    return answer


def how_much_lessons(self_para, student_username):
    """
    :param self_para: The root object of Tkinter library.
    :param student_username: The username of the student whose amount of lessons are being checked.
    Also used to check if the student is removed.
    :return: The amount of lessons the student had.
    """
    if student_username == "":
        return []
    client_socket.send(f"{Enum.HOW_MUCH_LESSONS}*{student_username}".encode())
    answer = client_socket.recv(1024).decode()

    if answer == "The Previous Frame":
        handle_student_connection_status(self_para, student_username, 1)  # option0-removed while being disconnected from the system.

        # In case, for some reason, the thread that has been activated on
        # "The Previous Frame" func, will cause socket collisions.

    return int(answer)


def add_feedbacks(student_username, lesson_number_entry, verbal_feedback_entry, quantitative_feedback_entry):
    """
    :param student_username: Entry widget for username.
    :param lesson_number_entry: Entry widget for lesson number.
    :param verbal_feedback_entry: Entry widget for verbal feedback.
    :param quantitative_feedback_entry: Entry widget for quantitative feedback.
    Checks if all the required data is available. If not, the user will be informed through dedicated message boxes.
    If everything is okay, it adds the written feedback to the feedback table and informs the teacher about it.
    """
    # Get the values entered by the teacher
    lesson_number = lesson_number_entry.get()
    verbal_feedback = verbal_feedback_entry.get()
    quantitative_feedback = quantitative_feedback_entry.get()

    if student_username == "No Students Available":
        messagebox.showerror("Error", "Please connect at least one student to the system.")
    elif student_username == "":
        messagebox.showerror("Error", "Please choose your current student.")
    elif lesson_number == "":
        messagebox.showerror("Error", "Please choose the current lesson number.")
    elif verbal_feedback == "":
        messagebox.showerror("Error", "Please enter your verbal feedback.")
    elif quantitative_feedback == "":
        messagebox.showerror("Error", "Please enter your quantitative feedback.")
    else:
        # Send feedback data to the server
        client_socket.send(f"{Enum.ADD_FEEDBACK}*{student_username}*{lesson_number}*"
                           f"{verbal_feedback}*{quantitative_feedback}".encode())
        messagebox.showinfo("Success", "You successfully sent your feedback. \n You can update it whenever you want.")

        # Reset the entry fields
        lesson_number_entry.set("")
        quantitative_feedback_entry.set("")
        verbal_feedback_entry.delete(0, "end")


def get_the_previous_frame(self_para, student_username):
    """
    :param self_para: The root object of Tkinter library.
    :param student_username: The username of the student who is being checked for removal.
    It's activated as a thread. Navigates the student to the "handle_student_connection_status"
    function when their teacher removes them from the system.
    """
    template = ""
    text_message = "The Previous Frame"
    while template != text_message:
        template = client_socket.recv(1024).decode()

        # In order to avoid socket collisions, it is necessary to stop the thread before other functions
        # are called. This can be seen more clearly in "Windows.py".
        if template == "STOP THE THREAD":
            return

    handle_student_connection_status(self_para, student_username, 1)


def stopping_the_removing_thread():
    """
    Stops the thread activated on the "the_previous_frame" function in order to avoid socket collisions.
    """
    client_socket.send(f"{Enum.STOP_THE_THREAD}".encode())


def handle_student_connection_status(self_para, student_username, num):
    """
    :param self_para: The root object of Tkinter library.
    :param student_username: The username of the student.
    :param num: num = 1 when the student has been removed while being connected.
    Then, it's navigates the student to the "JoiningStudentFrame" with option 2 (removed while connected).

    This function can get called from two places:
    -During login to the system, checks if the user has been removed since the last time they logged in (num=1).
    -The "get_the_previous_frame" function calls this func when the student gets removed while being connected.

    If the student removed, it informs the student and offers to download feedback data.
    If the user chooses to download, creates and downloads an Excel file with the feedback data.
    """
    client_socket.send(f"{Enum.IF_REMOVED}*{student_username}".encode())
    answer = pickle.loads(client_socket.recv(1024))
    if answer == ["False"]:  # means the user haven't been removed since the last time they logged in.
        return
    messagebox.showinfo("Success", f"{student_username}, You have been removed by your teacher")
    yes_or_no = messagebox.askyesno("Download a file", "Do you want to download an excel file with the feedback data?")
    if yes_or_no:
        answer = [(tup[:-1]) for tup in answer]  # removes the "removed" column from the feedback table
        File.create_and_download_file(answer)

    if num == 1:
        Windows.JoiningStudentFrame(self_para, student_username, 2)  # option2-you have been removed while connected


def add_lesson(self_para, student_username, teacher_username):
    """
    :param self_para: The root object of Tkinter library.
    :param student_username: The username of student for whom a lesson is being added.
    :param teacher_username: the username of the teacher adding the lesson for the student.
    Adds a row to the specific student in the feedbacks table with the student and teacher usernames,
    and the added lesson number.
    Additionally, the function calls the "variable_lesson_number" func,
    which updates the student's number of lessons in real-time in the "TeacherOptionsFrame".
    """
    if student_username == "":
        messagebox.showerror("Error", "Please choose your current student.")
    else:
        client_socket.send(f"{Enum.ADD_LESSON}*{student_username}*{teacher_username}".encode())
        self_para.variable_lesson_number()


def last_entered_lesson(student_username):
    """
    There is three ways for the teacher and the student to track  their last entered lesson:
    -The teacher can create lessons and immediately enter the feedback for them;
     so the last entered lesson will also be the last lesson in the lessons list.
    -The teacher and the student can track the last entered lesson
     using their own method, such as using a diary or a calendar.
    -The teacher and the student can use the "last entered lesson" tool, which shows the last entered lesson.
     Import Note: This tool works only when there is feedbacks for all lessons in sequential order.
     Otherwise, there is no way to determine which lesson number the teacher and the student are referring to.

    :param student_username: The username of the student whose last entered lesson is being checked.
    :return: The last lesson on which feedback was entered by the teacher (assuming feedbacks are sequential).
    """
    client_socket.send(f"{Enum.LAST_ENTERED_LESSON}*{student_username}".encode())
    return client_socket.recv(1024).decode()


def friends_list(self_para, student_username):
    """
    :param self_para: The root object of Tkinter library.
    :param student_username: The username of the student who is being checked for removal.
    :return: Returns the list of all friends connected to the system.
    """
    client_socket.send(f"{Enum.FRIEND_LIST}".encode())
    answer = pickle.loads(client_socket.recv(1024))

    # In case, for some reason, the thread that has been activated on
    # "The Previous Frame" func, will cause socket collisions.
    if answer == "The Previous Frame":
        handle_student_connection_status(self_para, student_username, 1)  # option0-removed while being disconnected from the system.

        ## it gives pickle, but the result is not pickle. may do a problem

    else:
        return answer


def feedbacks_per_lesson(self_para, student_username, lesson_number):
    """
    :param self_para: The root object of Tkinter library.
    :param student_username: The username of the student who wants to get the feedback about themselves.
    Also used to check if the student is removed.
    :param lesson_number: The lesson number the student wants to see feedback for.
    :return: The verbal and quantitative feedback for the chosen lesson.
    """
    client_socket.send(f"{Enum.FEEDBACKS_PER_LESSON}*{student_username}*{lesson_number}".encode())
    answer = client_socket.recv(1024).decode()

    # In case, for some reason, the thread that has been activated on
    # "The Previous Frame" func, will cause socket collisions.
    if answer == "The Previous Frame":
        handle_student_connection_status(self_para, student_username, 1) # option0-removed while being disconnected from the system.

    else:
        return answer


def share_feedback_with_friend(self_para, lesson_number, student_username, friend_username_entry, listbox):
    """
    :param self_para: The root object of Tkinter library.
    :param lesson_number: The lesson number the student want shares the feedback on with their friend.
    :param student_username: The student who wants to share the feedback data with their friend.
    :param friend_username_entry: The selected friend's username entry.
    :param listbox: The listbox widget containing friend usernames.
    :return: If not all the data is in the func hands & if the friend is already logged out,
    the user will be informed through dedicated message boxes. If everything is okay,
    the feedback data will be sent to the friend.

    """
    stopping_the_removing_thread()  # stops the thread activated on the "the_previous_frame" func in order
    # to avoid socket collisions.

    if not friend_username_entry:
        messagebox.showerror("Error", "Please chose your friend username.")
    friend_username = listbox.get(friend_username_entry[0])
    if lesson_number == "":
        messagebox.showerror("Error", "Please choose the lesson number.")
    elif friend_username not in friends_list(self_para, student_username):
        messagebox.showerror("Error", "Your friend is not connected anymore. Please choose"
                                      " another friend or try again later.")
    else:
        messagebox.showinfo("Success", "You successfully shared the feedback with your friend.")
        client_socket.send(f"{Enum.SHARE_FEEDBACK_WITH_FRIEND}*{lesson_number}*{student_username}*{friend_username}".encode())

    threading.Thread(target=get_the_previous_frame, args=(self_para, student_username)).start()
    # starts the thread once again


def friend_gets_feedback(self_para, friend_username):
    """
    :param self_para: The root object of Tkinter library.
    :param friend_username: The username of the friend who gets the feedback data from the student.
    :return: It's activated as a thread. Navigates the student to
    the "update_feedback_text" func in "FriendsGetTheFeedbackFrame", which shows the feedback on their screen.
    """
    lst = ["", "", "", ""]
    text_message = "Feedback"
    while lst[0] != text_message and lst[1] != friend_username:
        template = client_socket.recv(1024).decode()
        lst = template.split("%")
    Windows.FriendsGetTheFeedbackFrame.update_feedback_text(self_para, friend_username, f"{lst[2]}: {lst[3]}")


def remove_student(self_para, teacher_username, student_username):
    """
    :param self_para: The root object of Tkinter library.
    :param teacher_username: The username of the teacher who removes their student.
    :param student_username: The username of the student being removed.
    :return: Asks the teacher if she really wants to remove the student, and if so,
    negatives them to the "TeacherFeedbacksFrame".
    """
    if student_username == "":
        messagebox.showerror("Error", "Please choose a student")
    else:
        answer = messagebox.askyesno("A Warning", "Are you sure you want to continue?")
        if answer:
            messagebox.showinfo("Message", f"You have successfully removed {student_username}!")
            client_socket.send(f"{Enum.REMOVE_STUDENT}*{student_username}".encode())
            Windows.TeacherFeedbacksFrame(self_para, teacher_username)


def logout_button(username, self_para):
    """
    :param username: The username of the user who wants to log out from the system.
    :param self_para: The root object of Tkinter library.
    Logs out the student from the system & removes them from the "connected users" dictionary (dictionary is in server).
    """
    messagebox.showinfo("Success", "You have successfully logged out from the system")
    client_socket.send(f"{Enum.LOGOUT}*{username}".encode())
    self_para.destroy()
    Windows.LoginWindow()


if __name__ == "__main__":
    """
    Entry point of the application. Creates and displays the LoginWindow when the script is executed directly.
    """
    Windows.LoginWindow()
