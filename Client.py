import socket
import time
from tkinter import messagebox

import File
import Windows
from Objects import Enum
import pickle
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 4444))


def is_fit_password(password):
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
    #elif len(username) < 12 or username[9] != "_" or not username[0:8].isdigit():
        #messagebox.showerror("Error", "Your username does not fit the pattern. Please try again.")
    #elif not is_fit_password(password):
        #messagebox.showerror("Error", "Your password is not strong enough. Please follow the conditions.")

    else:
        client_socket.send(f"{Enum.REGISTRATION}*{username}*{password}*{user_type}".encode())
        answer = client_socket.recv(1024).decode()

        if answer in ["Student", "Teacher", "Friend"]:
            messagebox.showinfo("Excellent!", "You have successfully registered")
            division_between_clients(user_type, username, self_para)
        elif answer == "user already exists":
            messagebox.showerror("Error", "The user already exists.")
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

        if answer in ["Student", "Teacher", "Friend"]:
            messagebox.showinfo("Excellent!", "You have successfully logged in")
            division_between_clients(answer, username, self_para)
        elif answer == "user doesn't exist":
            messagebox.showerror("False details", "This user does not exist.")
            username_entry.delete(0, "end")
        elif answer == "wrong password":
            messagebox.showerror("False Details", "This password is wrong. Please try again.")
            password_entry.delete(0, "end")


def division_between_clients(user_type, username, self_para):
    """
    :param user_type: represents the user type (student, teacher, friend)
    :param username: represents the username
    :param self_para: the root object of Tk inter library
    :return: routes each user to its own path by his type
    """
    if user_type == "Student":
        if passed_step2_in_registration(username) == "True":
            remove_and_download(self_para, username, 0)
            Windows.StudentFeedbacksFrame(self_para, username, 0)
        else:
            if passed_step1_in_registration(username) == "1":
                if remove_and_download(self_para, username, 0) != ["False"]:
                    Windows.JoiningStudentFrame(self_para, username, 2)
                else:
                    Windows.JoiningStudentFrame(self_para, username, 1) ##still waits for a connection with his teacher
            else:
                Windows.JoiningStudentFrame(self_para, username, 0) ##didn't choose YES or NO
    if user_type == "Teacher":
        if passed_step2_in_registration(username) == "True":
            Windows.TeacherFeedbacksFrame(self_para, username)
        else:
            Windows.TeacherOptionsFrame(self_para, username)
    if user_type == "Friend":
        Windows.FriendsGetTheFeedbackFrame(self_para, username)


def passed_step1_in_registration(username):
    """
    :param username: represents the username
    :return: did the user already passed step number 1 in the registration to the system - Did he find a teacher/student
    """
    client_socket.send(f"{Enum.STEP1}*{username}".encode())
    return client_socket.recv(1024).decode()


def passed_step2_in_registration(username):
    """
    :param username: represents the username
    :return: did the user already passed step number 2 in the registration to the system - Did he find a teacher/student
    """
    client_socket.send(f"{Enum.STEP2}*{username}".encode())
    return client_socket.recv(1024).decode()


def list_of_students():
    """
    :return: the list of all the students - Those who chose "Yes" so there accounts will be hidden while disconnected &
     Those who chose the opposite. Therefore, students who already connected with their teacher will not be in the list.
    """
    client_socket.send(f"{Enum.STUDENT_LIST}".encode())
    return pickle.loads(client_socket.recv(1024))


def teacher_chose_student(self_para, teacher_username, student_username_entry, listbox):
    """
    :param self_para: the root object of Tk inter library
    :param teacher_username: represents the teacher username
    :param student_username: represents the student username the teacher chose
    :return: pass the teacher to the feedbacks frame
    """
    if not student_username_entry:
        messagebox.showerror("Error", "You need to choose a student")
    student_username = listbox.get(student_username_entry[0])
    if student_username not in list_of_students():
        messagebox.showerror("Error", "This student is not on the options anymore. Please choose"
                                      " another student or try again later.")
    else:
        client_socket.send(f"{Enum.THE_NEXT_FRAME}*{student_username}*{teacher_username}".encode())
        Windows.TeacherFeedbacksFrame(self_para, teacher_username)


def add_to_clients_messages(self_para, answer, student_username):
    """
    :param self_para: the root object of Tk inter library
    :param answer: represents if the client want to hide his account while disconnected
    :param student_username: represents the username of the student
    :return: bring the student back to the JoiningStudentFrame to wait until connection with teacher
    """
    warning = messagebox.askyesno("A Warning", "Are you sure? You can only choose one time")
    if warning:
        if answer:
            messagebox.showinfo("Excellent", "You successfully chose YES!")
            client_socket.send(f"{Enum.YES}*{student_username}".encode())
        else:
            messagebox.showinfo("Excellent", "You successfully chose NO!")
            client_socket.send(f"{Enum.NO}*{student_username}".encode())
        Windows.JoiningStudentFrame(self_para, student_username, 1)


def get_the_next_frame(self_para, student_username, num):
    """
    :param self_para: the root object of Tk inter library
    :param student_username: represents the username of the student
    :return: pass the student to the feedback frame when the teacher connects him
    """
    template = ""
    text_message = "The Next Frame"
    while template != text_message:
        template = client_socket.recv(1024).decode()
    if num == 0:
        Windows.StudentFeedbacksFrame(self_para, student_username, 0)


def get_the_previous_frame(self_para, student_username):
    """
    :param self_para: the root object of Tk inter library
    :param student_username: represents the username of the student
    :return: pass the student to the feedback frame when the teacher connects him
    """
    template = ""
    text_message = "The Previous Frame"
    while template != text_message:
        template = client_socket.recv(1024).decode()
        if template == "HEY":
            return
    remove_and_download(self_para, student_username, 1)

def remove_and_download(self_para, student_username, num):
    client_socket.send(f"{Enum.IF_REMOVED}*{student_username}".encode())
    answer = pickle.loads(client_socket.recv(1024))
    if answer == ["False"]:
        return
    messagebox.showinfo("Excellent!", f"{student_username}, You have been removed by your teacher")
    yes_or_no = messagebox.askyesno("Download a file", "Do you want to download an excel file with the feedbacks?")
    if yes_or_no:
        answer = [(tup[:-1]) for tup in answer] ## removes the 'remove' line from the feedback tavla
        File.create_and_download_file(answer)
    if num == 1:
        Windows.JoiningStudentFrame(self_para, student_username, 2) ##you have been removed while connected
def list_of_students_per_teacher(teacher_username):
    """
    :param teacher_username: represents the username of the teacher
    :return: list of students that connected to a teacher
    """
    client_socket.send(f"{Enum.STUDENTS_FOR_TEACHER}*{teacher_username}".encode())
    check = pickle.loads(client_socket.recv(1024))
    check = [item for t in check for item in t]
    return check


def add_feedbacks(student_username, lesson_number_entry, verbal_feedback_entry, quantitative_feedback_entry):
    """
    :param student_username: represents the username of the student
    :param lesson_number: represents the lesson number the teacher chose
    :param verbal_feedback: represents the verbal feedback the teacher wrote
    :param quantitative_feedback: represents the quantitative feedback the teacher chose
    :return: it adds the feedback to the feedback chart
    """
    lesson_number = lesson_number_entry.get()
    verbal_feedback = verbal_feedback_entry.get()
    quantitative_feedback = quantitative_feedback_entry.get()

    if student_username == "No Students Available":
        messagebox.showerror("Error", "Please add at least 1 student to the system.")
    elif student_username == "":
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
        messagebox.showinfo("Excellent", "You successfully sent your feedback \n You can update it whenever you want.")
        lesson_number_entry.set("")
        quantitative_feedback_entry.set("")
        verbal_feedback_entry.delete(0, "end")


def ty():
    client_socket.send(f"{Enum.HEY}".encode())


def add_lesson(self_para, student_username, teacher_username):
    """
    :param self_para: the root object of Tk inter library
    :param student_username: represents the username of the student
    :param teacher_username: represents the username of the teacher
    :return: it adds a row to the specif student in the feedback chart
    """
    if student_username == "":
        messagebox.showerror("Error", "You need to choose your current student")
    else:
        client_socket.send(f"{Enum.ADD_LESSON}*{student_username}*{teacher_username}".encode())
        self_para.variable_lesson_number()


def how_much_lessons(self_para, student_username):
    """
    :param student_username: represents the username of the student
    :return: the amount of lessons for the student
    """
    if student_username == "":
        return []
    client_socket.send(f"{Enum.HOW_MUCH_LESSONS}*{student_username}".encode())
    answer = client_socket.recv(1024).decode()
    if answer == "The Previous Frame":
        remove_and_download(self_para, student_username, 1)
    return int(answer)


def last_lesson(student_username):
    """
    :param student_username: represents the username of the student
    :return: the last lesson the teacher entered feedback to (Assuming the lessons are entered in numbered form)
    """
    client_socket.send(f"{Enum.LAST_LESSON}*{student_username}".encode())
    return client_socket.recv(1024).decode()


def friends_list(self_para, student_username):
    """
    :return: the list of the usernames of the "Friend" type users who are connected
    """
    client_socket.send(f"{Enum.FRIEND_LIST}".encode())
    answer = pickle.loads(client_socket.recv(1024))
    if answer == "The Previous Frame":
        remove_and_download(self_para, student_username, 1) ##it gives pickle, but the result is not pickle. may do a problem
    else:
        return answer


def feedbacks_per_lesson(self_para, student_username, lesson_number):
    """
    :param student_username: represents the username of the student
    :param lesson_number: represents the lesson number the student wants to see the feedback about
    :return: the feedback for the lesson the student chose
    """
    client_socket.send(f"{Enum.FEEDBACKS_PER_LESSON}*{student_username}*{lesson_number}".encode())
    answer = client_socket.recv(1024).decode()
    if answer == "The Previous Frame":
        remove_and_download(self_para, student_username, 1)
    else:
        return answer


def share_feedback_with_friend(self_para, lesson_number, student_username, friend_username_entry, listbox):
    """
    :param lesson_number:
    :param student_username:
    :param friend_username:
    :return:
    """
    ty()
    if not friend_username_entry:
        messagebox.showerror("Error", "Please chose your friend username.")
    friend_username = listbox.get(friend_username_entry[0])
    if lesson_number == "":
        messagebox.showerror("Error", "Please choose the lesson number.")
    elif friend_username not in friends_list(self_para, student_username):
        messagebox.showerror("Error", "Your friend is not connected anymore. Please choose"
                                      " another friend or try again later.")
    else:
        messagebox.showinfo("Excellent!", "You successfully shared the feedback with your friend.")
        client_socket.send(f"{Enum.SHARE_FEEDBACK_WITH_FRIEND}*{lesson_number}*{student_username}*{friend_username}".encode())

    threading.Thread(target=get_the_previous_frame, args=(self_para, student_username)).start()


def friend_gets_feedback(self_para, friend_username):
    """
    :param self_para: the root object of Tk inter library
    :param friend_username: represents the username of the student
    :return: pass the student to the feedback frame when the teacher connects him
    """
    lst = ["", "", "", ""]
    text_message = "Feedback"
    while lst[0] != text_message and lst[1] != friend_username:
        template = client_socket.recv(1024).decode()
        lst = template.split("&")
    Windows.FriendsGetTheFeedbackFrame.update_feedback_text(self_para, friend_username, f"{lst[2]}: {lst[3]}")


def remove_student(master, teacher_username, student_username):
    if student_username == "":
        messagebox.showerror("Error", "Please choose a student")
    else:
        answer = messagebox.askyesno("A Warning", "Are you sure you want to continue?")
        if answer:
            messagebox.showinfo("Message", f"You have successfully removed {student_username}!")
            client_socket.send(f"{Enum.REMOVE_STUDENT}*{student_username}".encode())
            Windows.TeacherFeedbacksFrame(master, teacher_username)


def logout_button(username, self_para):
    """
    :param username: represents the username of the client
    :param self_para: the root object of Tk inter library
    :return: disconnects the student from the system & removes him from the connected clients dictionary
    """
    messagebox.showinfo("Excellent!", "You have successfully logout from the system")
    client_socket.send(f"{Enum.DISCONNECT}*{username}".encode())
    self_para.destroy()
    Windows.LoginWindow()


if __name__ == "__main__":
    Windows.LoginWindow()
