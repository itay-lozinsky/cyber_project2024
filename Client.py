import socket
from tkinter import messagebox
import Windows
from Objects import Enum
import pickle
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 4444))


def registration_check(username_entry, password_entry, type_entry, self_para):
    """
    :param username_entry: represents the text the client wrote in the "username" field
    :param password_entry: represents the text the client wrote in the "password" field
    :param type_entry: represents the option the client chose in the "type" field
    :param self_para: the root object of Tk inter library
    :return: pass the client to the "division between clients" function
    """
    username = username_entry.get()
    password = password_entry.get()
    user_type = type_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "You need to enter your details.")

    elif user_type == "":
        messagebox.showerror("Error", "You need to choose your user type.")

    else:
        client_socket.send(f"{Enum.REGISTRATION}*{username}*{password}*{user_type}".encode())
        answer = client_socket.recv(1024).decode()

        if answer in ["Student", "Teacher", "Friend"]:
            division_between_clients(user_type, username, self_para)
        else:
            messagebox.showerror("Error", "The user already exists")
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")


def login_check(username_entry, password_entry, self_para):
    """
    :param username_entry: represents the text the client wrote in the "username" field
    :param password_entry: represents the text the client wrote in the "password" field
    :param self_para: the root object of Tk inter library
    :return: pass the client to the "division between clients" function
    """
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "You need to enter your details.")

    else:
        client_socket.send(f"{Enum.CONNECTING}*{username}*{password}".encode())
        answer = client_socket.recv(1024).decode()

        if answer == "Student" or answer == "Teacher" or answer == "Friend:":
            messagebox.showinfo("Excellent!", "You have been successfully logged in")
            division_between_clients(answer, username, self_para)
        elif answer == "user doesnt exist":
            messagebox.showerror("False details", "User doesn't exist")
        else:
            messagebox.showerror("False Details", "Your password is wrong. Please try again")
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")


def division_between_clients(user_type, username, self_para):
    """
    :param user_type: represents the user type (student, teacher, friend)
    :param username:  represents the username
    :param self_para: the root object of Tk inter library
    :return: routes each user to its own path by his type
    """
    if user_type == "Student":
        if check_if_first_time_connected(username) == "True":
            Windows.StudentFeedbacksFrame(self_para, username)
        else:
            Windows.JoiningStudentFrame(self_para, username)
    if user_type == "Teacher":
        if check_if_first_time_connected(username) == "True":
            Windows.TeacherFeedbacksFrame(self_para, username)
        else:
            Windows.TeacherOptionsFrame(self_para, username)
    if user_type == "Friend":



def the_user_is_joined(student_username):
    """
    :return: checks if it's the first time the client connected to the system
    """
    client_socket.send(f"{Enum.IS_JOINED}*{student_username}".encode())
    return client_socket.recv(1024).decode()


def list_of_students():
    """
    :return: the list of all the students - Those who chose "Yes" so there account will be hidden while disconnected &
     Those who chose the opposite
    """
    client_socket.send(f"{Enum.STUDENT_LIST}".encode())
    check = pickle.loads(client_socket.recv(1024))
    return check


def check_if_connected_and_error(self_para, teacher_username, student_username):
    """
    :param self_para: the root object of Tk inter library
    :param teacher_username: represents the teacher username
    :param student_username: represents the student username the teacher chose
    :return: None
    """
    if student_username == "":
        messagebox.showerror("Error", "You need to choose a student")
    elif student_username not in list_of_students():
        messagebox.showerror("Error", "This students is not on the options anymore. Please choose another student.")
    else:
        client_socket.send(f"{Enum.THE_NEXT_FRAME}*{student_username}*{teacher_username}".encode())
        Windows.TeacherFeedbacksFrame(self_para, teacher_username)


def add_to_clients_messages(self_para, answer, student_username):
    """
    :param self_para: gh
    :param answer: represents if the client want to hide his account while disconnected
    :param student_username: represents the username of the student
    :return: None
    """
    if answer:
        client_socket.send(f"{Enum.YES}*{student_username}".encode())
    else:
        client_socket.send(f"{Enum.NO}*{student_username}".encode())
    Windows.JoiningStudentFrame(self_para, student_username)


def get_the_next_frame(self_para, username, text_message):
    template = ""
    #text_message = "The Next Frame"
    while template != text_message:
        template = client_socket.recv(1024).decode()
    if text_message == "The Next Frame":
        Windows.StudentFeedbacksFrame(self_para, username)
    else:
        self.feedback_text.config(state="normal")
        return client_socket.recv(1024).decode()
        self.feedback_text_content = Client.feedbacks_per_lesson(self.moshe, self.lesson_number)

        if self.feedback_text_content == "No Data":
            message = f"No feedback available yet for lesson number {self.lesson_number}\n"
        else:
            message = f"Teacher's feedback for lesson number {self.lesson_number}: {self.feedback_text_content}\n"

        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state="disabled")


def list_of_students_for_teacher(teacher_username):
    client_socket.send(f"{Enum.STUDENTS_FOR_TEACHER}*{teacher_username}".encode())
    check = pickle.loads(client_socket.recv(1024))
    check = [item for t in check for item in t]
    return check


def add_feedbacks(student_username, lesson_number, verbal_feedback, quantitative_feedback):
    if student_username == "":
        messagebox.showerror("Error", "You need to choose your current student")
    elif lesson_number == "":
        messagebox.showerror("Error", "You need to choose the current lesson number")
    elif verbal_feedback == "":
        messagebox.showerror("Error", "You need to enter your verbal feedback")
    elif quantitative_feedback == "":
        messagebox.showerror("Error", "You need to enter your quantitative feedback")
    else:
        client_socket.send(f"{Enum.ADD_FEEDBACKS}"
        f"*{student_username}*{lesson_number}*{verbal_feedback}*{quantitative_feedback}".encode())


def check_if_first_time_connected(teacher_username):
    client_socket.send(f"{Enum.CHECK_IF_FIRST_TIME_CONNECTED}*{teacher_username}".encode())
    return client_socket.recv(1024).decode()


def add_lesson(self_para, student_username, teacher_username):
    if student_username == "":
        messagebox.showerror("Error", "You need to choose a student")
    else:
        client_socket.send(f"{Enum.ADD_LESSON}*{student_username}*{teacher_username}".encode())
        self_para.last1()


def how_much_lessons(student_username):
    if student_username == "":
        return []
    client_socket.send(f"{Enum.HOW_MUCH_LESSONS}*{student_username}".encode())
    return pickle.loads(client_socket.recv(1024))


def last_lesson(student_username):
    client_socket.send(f"{Enum.LAST_LESSON}*{student_username}".encode())
    return client_socket.recv(1024).decode()

def friend_list():
    client_socket.send(f"{Enum.FRIEND_LIST}".encode())
    check = pickle.loads(client_socket.recv(1024))
    return check


def disconnect_button(username, self_para):
    messagebox.showinfo("Excellent", "You have successfully disconnected from the system")
    client_socket.send(f"{Enum.DISCONNECT}*{username}".encode())
    #client_socket.close()


def feedbacks_per_lesson(student_username, lesson_number):
    client_socket.send(f"{Enum.FEEDBACKS_PER_LESSON}*{student_username}*{lesson_number}".encode())
    return client_socket.recv(1024).decode()

def share_feedback_with_friend(lesson_number, student_username, friend_username):
    if friend_username.get() == "" or lesson_number.get() == "":
        messagebox.showerror("Error", "Please enter the details.")
    elif friend_username not in friend_list():
        messagebox.showerror("Error", "Your friend is not connected anymore. Please try again later.")
    else:
        client_socket.send(f"{Enum.SHARE_FEEDBACK_WITH_FRIEND}*{lesson_number.get()}*{student_username}*{friend_username.get()}".encode())


if __name__ == "__main__":
    Windows.LoginWindow()
