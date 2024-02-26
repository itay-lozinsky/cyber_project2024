import tkinter as tk
from tkinter import messagebox
from tkinter import *
import Client
import threading


class BaseWindow(tk.Tk):
    """
    initializes the base window
    """
    def __init__(self, title, width=700, height=600):
        super().__init__()
        self.title(f'{title}')
        self.geometry(f'{width}x{height}')
        self.configure(bg='#3498db')  # Set background color to a shade of blue


class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__("Driving Lessons System")

        login_frame = tk.Frame(self, bg='#3498db')  # Set frame background color
        login_frame.pack(padx=20, pady=20)

        label_font_size = 16
        entry_font_size = 14
        button_font_size = 14

        tk.Label(login_frame, text="User Name:", font=("Arial Bold", label_font_size), bg='#3498db', fg='white').pack(side="top")
        username_entry = tk.Entry(login_frame, font=("Arial", entry_font_size))
        username_entry.pack(side="top", pady=5)

        tk.Label(login_frame, text="Password:", font=("Arial Bold", label_font_size), bg='#3498db', fg='white').pack(side="top")
        password_entry = tk.Entry(login_frame, show="*", font=("Arial", entry_font_size))
        password_entry.pack(pady=5)

        tk.Button(login_frame, text="Login", font=("Arial Bold", button_font_size), width=15, command=lambda: Client.login_check(username_entry, password_entry, self)).pack(pady=10)

        tk.Button(login_frame, text="You don't have an account? Click here!", font=("Arial", max(12, int(button_font_size * 0.7))), width=40, command=lambda: RegisterFrame(self)).pack()

        self.mainloop()


class RegisterFrame(tk.Frame):
    """
    creates the registration frame
    """
    def __init__(self, master):
        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        lbl_num = tk.Label(self, text="Username:", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        username = tk.Entry(self)
        username.pack(side="top")

        lbl_num = tk.Label(self, text="Password:", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        password = tk.Entry(self, show="*")
        password.pack()

        clicked = tk.StringVar()
        type_option = tk.OptionMenu(self, clicked, "Student", "Teacher", "Friend")
        type_option.pack()

        btn_click = tk.Button(self, text="Register", height=3, font=("Ariel Black", 15), width=10,
                              command=lambda: Client.registration_check(username, password, clicked, master))
        btn_click.pack()


class JoiningStudentFrame(tk.Frame):
    """
    creates the joining student frame. In this frame the student choose if he wants to hide his account while disconnected
    """
    def __init__(self, master, student_username):
        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        btn_click = tk.Button(self, text="Disconnect", height=3, font=("Ariel Black", 15), width=10, command=lambda: Client.
                              disconnect_button(student_username, master))
        btn_click.pack()

        if Client.the_user_is_joined(student_username) == "False":

            self.lbl_num = tk.Label(self, text=f"Welcome {student_username}! Do you want to hide your account \n "
                                          f"while you are disconnected?", height=3, font=("Ariel Bold", 20))
            self.lbl_num.pack(side="top")

            self.btn_click = tk.Button(self, text="Yes", height=3, font=("Ariel Black", 15), width=10, command=lambda: Client.
                                       add_to_clients_messages(master, True, student_username))
            self.btn_click.pack()

            self.btn_click1 = tk.Button(self, text="No", height=3, font=("Ariel Black", 15), width=10, command= lambda: Client.
                                        add_to_clients_messages(master, False, student_username))
            self.btn_click1.pack()

            lbl_num1 = tk.Label(self, text=f"After you choose, \n"
                                          f" please wait until the teacher connects with you.", height=3,
                               font=("Ariel Bold", 20))
            lbl_num1.pack()

        else:
            threading.Thread(target=Client.get_the_next_frame, args=(master, student_username)).start()

            lbl_num = tk.Label(self, text=f"Thanks! Please wait until the teacher connects with you, \n"
                                          f" Meanwhile you can disconnect.", height=3,
                               font=("Ariel Bold", 20))
            lbl_num.pack()


class TeacherOptionsFrame(tk.Frame):
    """
    creates the teacher options frame. In this frame the teacher choose his students
    """
    def __init__(self, master, teacher_username):
        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        disconnect_button(teacher_username, self)

        btn_click = tk.Button(self, text="Refresh", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        TeacherOptionsFrame(master, teacher_username))
        btn_click.pack(side="top")

        if Client.check_if_first_time_connected(teacher_username) == "True":
            btn_click = tk.Button(self, text="Back", height=3, font=("Ariel Black", 15), width=10, command=lambda:
            TeacherFeedbacksFrame(master, teacher_username))
            btn_click.pack(side="top")

        lbl_num = tk.Label(self, text=f"Welcome {teacher_username}!"
                                      f" Please choose your student:", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        check = Client.list_of_students()

        if check:
            clicked = tk.StringVar()
            type_option = tk.OptionMenu(self, clicked, *check)
            type_option.pack()
            btn_click = tk.Button(self, text="Enter", height=3, font=("Ariel Black", 15), width=10, command=lambda:
            Client.check_if_connected_and_error(master, teacher_username, clicked.get()))
            btn_click.pack()

        else:
            lbl_num = tk.Label(self, text=f"Sorry. There are no students ready to connect right now! "
                                          f"\n Please try again later", height=3, font=("Ariel Bold", 20))
            lbl_num.pack()


class StudentFeedbacksFrame(tk.Frame):
    def __init__(self, master, student_username):
        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        disconnect_button(student_username, self)

        self.btn_click = tk.Button(self, text="Refresh", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        StudentFeedbacksFrame(master, student_username))
        self.btn_click.pack(side="top")

        self.lbl_num = tk.Label(self, text=f"Hello {student_username}!"
                                      f" Please choose the lesson number you \n want to get feedback on", height=3, font=("Ariel Bold", 20))
        self.lbl_num.pack(side="top")

        self.check = list(range(1, Client.how_much_lessons(student_username)+1))
        self.chosen_lesson_number = tk.StringVar(self)
        self.type_option = tk.OptionMenu(self, self.chosen_lesson_number, *self.check)
        self.type_option.pack()

        self.btn_click = tk.Button(self, text="Enter", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        self.enter())
        self.btn_click.pack()

        self.feedback_text = Text(width=80, height=100)
        self.feedback_text.pack()
        self.feedback_text.config(state="disabled")
        self.moshe = student_username

    def enter(self):
        self.feedback_text.config(state="normal")
        self.lesson_number = self.chosen_lesson_number.get()
        self.feedback_text_content = Client.feedbacks_per_lesson(self.moshe, self.lesson_number)

        if self.feedback_text_content == "No Data":
            message = f"No feedback available yet for lesson number {self.lesson_number}\n"
        else:
            message = f"Teacher's feedback for lesson number {self.lesson_number}: {self.feedback_text_content}\n"

        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state="disabled")


class TeacherFeedbacksFrame(tk.Frame):
    def last1(self, *args):
        student_username = self.clicked.get()
        options = list(range(1, Client.how_much_lessons(student_username)+1))
        self.lesson_number.set("")
        self.type_option2["menu"].delete(0, "end")
        for option in options:
            self.type_option2["menu"].add_command(label=option, command=tk._setit(self.lesson_number, option))

    def __init__(self, master, teacher_username):

        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        disconnect_button(teacher_username, self)

        btn_click = tk.Button(self, text="Add Student", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        TeacherOptionsFrame(master, teacher_username))
        btn_click.pack(side="top")

        btn_click = tk.Button(self, text="Add Lesson", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        Client.add_lesson(self, self.clicked.get(), teacher_username))
        btn_click.pack(side="top")

        btn_click = tk.Button(self, text="Last Lesson", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        last())
        btn_click.pack(side="top")

        lbl_num = tk.Label(self, text=f"Hello {teacher_username}! "
        f"Please choose your current student:", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        check = Client.list_of_students_for_teacher(teacher_username)
        self.clicked = tk.StringVar(self)
        self.type_option = tk.OptionMenu(self, self.clicked, *check)
        self.type_option.pack()
        self.clicked.trace_add("write", self.last1)

        lbl_num = tk.Label(self, text="Please choose the lesson number", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        self.lesson_number = tk.StringVar(self)
        self.type_option2 = tk.OptionMenu(self, self.lesson_number, "")
        self.type_option2.pack()

        lbl_num = tk.Label(self, text="Please enter your verbal & quantitative feedback", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        quantitative_feedback = tk.StringVar()
        one_to_ten = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        type_option = tk.OptionMenu(self, quantitative_feedback, *one_to_ten)
        type_option.pack()

        verbal_feedback = tk.Entry(self)
        verbal_feedback.pack(side="top")

        btn_click = tk.Button(self, text="Enter", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        Client.add_feedbacks(self.clicked.get(), self.lesson_number.get(), verbal_feedback.get(), quantitative_feedback.get()))
        btn_click.pack()

        def last():
            if self.clicked.get() == "":
                messagebox.showerror("Error", "Please choose a student")
            else:
                last_lesson = Client.last_lesson(self.clicked.get())
                if not hasattr(last, 'label_created'):
                    self.lbl_num = tk.Label(self, text=f"The last lesson you entered is: {last_lesson}", height=3,
                                       font=("Ariel Bold", 20))
                    self.lbl_num.pack(side="top")
                    last.label_created = True

                self.lbl_num.config(text=f"The last lesson you entered is: {last_lesson}")


class StudentSharesWithFriendFrame(tk.Frame):
    def __init__(self, master, student_username):

        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        disconnect_button(student_username, self)

        lbl_num = tk.Label(self, text=f"Please choose the friend user name & lesson number you want to share with him"
                        , height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        friend_username = tk.StringVar()
        check = Client.friend_list()
        type_option = tk.OptionMenu(self, friend_username, *check)
        type_option.pack()

        check = list(range(1, Client.how_much_lessons(student_username) + 1))
        lesson_number = tk.StringVar()
        type_option = tk.OptionMenu(self, lesson_number, *check)
        type_option.pack()


class FriendsFrame(tk.Frame):
    def __init__(self, master, friend_username):

        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        disconnect_button(friend_username, self)

        lbl_num = tk.Label(self, text=f"Welcome {friend_username}!"
                                      f" Here is the information your friends decided to share with you:", height=3,
                           font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        self.feedback_text = Text(width=80, height=100)
        self.feedback_text.pack()
        self.feedback_text.config(state="disabled")




def disconnect_button(username, self_para):
    btn_click = tk.Button(self_para, text="Disconnect", height=3, font=("Ariel Black", 15), width=10, command=lambda:
    Client.disconnect_button(username, self_para))
    btn_click.pack(side="top")
