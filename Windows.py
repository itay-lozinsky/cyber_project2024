import tkinter as tk
import Client
import Windows


class BaseWindow(tk.Tk):
    """
    initializes the base window
    """
    def __init__(self, title, width=700, height=600):
        super().__init__()
        self.title(f'{title}')
        self.geometry(f'{width}x{height}')


class LoginWindow(BaseWindow):
    """
    creates the GUI window & the login frame
    """
    def __init__(self):
        super().__init__("Driving Lessons System")
        login_frame = tk.Frame(self)
        login_frame.pack()
        lbl_num = tk.Label(login_frame, text="User Name:", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        username = tk.Entry(login_frame)
        username.pack(side="top")

        lbl_num = tk.Label(login_frame, text="Password:", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        password = tk.Entry(login_frame, show="*")
        password.pack()

        btn_click = tk.Button(login_frame, text="Login", height=3, font=("Ariel Black", 15), width=10, command=lambda: Client.login_check(username, password, self))
        btn_click.pack()

        register = tk.Button(login_frame, text="You don't have an account? Click here!", height=3, font=("Ariel Black", 15), width=40, command=lambda: RegisterFrame(self))
        register.pack()

        self.mainloop()


class RegisterFrame(tk.Frame):
    """
    creates the registration frame
    """
    def __init__(self, master):
        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        lbl_num = tk.Label(self, text="User Name:", height=3, font=("Ariel Bold", 20))
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
    def __init__(self, master, username):
        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        btn_click = tk.Button(self, text="Disconnect", height=3, font=("Ariel Black", 15), width=10, command=lambda: Client.
                              disconnected_button(username, master))
        btn_click.pack()

        lbl_num = tk.Label(self, text=f"Welcome {username}! Do you want to hide your account \n "
                                      f"while you are disconnected?", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        btn_click = tk.Button(self, text="Yes", height=3, font=("Ariel Black", 15), width=10, command=lambda: Client.
                              add_to_clients_messages(master, True, username))
        btn_click.pack()
        btn_click = tk.Button(self, text="No", height=3, font=("Ariel Black", 15), width=10, command= lambda: Client.
                              add_to_clients_messages(master, False, username))
        btn_click.pack()

        lbl_num = tk.Label(self, text=f"After you choose, \n"
                                      f" please wait until the teacher connects with you.", height=3,
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

        lbl_num = tk.Label(self, text="Please choose your student:", height=3, font=("Ariel Bold", 20))
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
    def __init__(self, master):
        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        lbl_num = tk.Label(self, text="HEY", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")


class TeacherFeedbacksFrame(tk.Frame):
    def __init__(self, master, teacher_username):
        super().__init__(master)
        master.winfo_children()[0].destroy()
        self.pack()

        btn_click = tk.Button(self, text="Disconnect", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        Client.disconnected_button(teacher_username, master))
        btn_click.pack(side="top")

        btn_click = tk.Button(self, text="Add Student", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        TeacherOptionsFrame(master, teacher_username))
        btn_click.pack(side="top")

        lbl_num = tk.Label(self, text=f"Hello {teacher_username}! "
        f"Please choose your current student:", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        check = Client.list_of_students_for_teacher(teacher_username)
        clicked = tk.StringVar()
        type_option = tk.OptionMenu(self, clicked, *check)
        type_option.pack()

        last_lesson = Client.last_lesson(clicked.get())
        lbl_num = tk.Label(self, text=f"The last lesson you entered is: {last_lesson}", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        lbl_num = tk.Label(self, text="Please choose the lesson number", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        lesson_number = tk.StringVar()
        one_to_ten = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        type_option = tk.OptionMenu(self, lesson_number, *one_to_ten)
        type_option.pack()

        lbl_num = tk.Label(self, text="Please enter your verbal & quantitative feedback", height=3, font=("Ariel Bold", 20))
        lbl_num.pack(side="top")

        quantitative_feedback = tk.StringVar()
        type_option = tk.OptionMenu(self, quantitative_feedback, *one_to_ten)
        type_option.pack()

        verbal_feedback = tk.Entry(self)
        verbal_feedback.pack(side="top")

        btn_click = tk.Button(self, text="Enter", height=3, font=("Ariel Black", 15), width=10, command=lambda:
        Client.add_feedbacks(clicked.get(), lesson_number.get(), verbal_feedback.get(), quantitative_feedback.get()))
        btn_click.pack()

