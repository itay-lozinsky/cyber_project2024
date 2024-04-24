import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import *
import Client
import threading
from tkinter import ttk
import WebScraping

class BaseWindow(tk.Tk):
    def __init__(self, title, width=700, height=1000):
        super().__init__()
        self.title(f'{title}')
        self.geometry(f'{width}x{height}')
        self.configure(bg='#3498db')  # Set background color to a shade of blue


class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__("Driving Lessons System")

        login_frame = tk.Frame(self, bg='#3498db')  # Set frame background color to blue
        login_frame.pack(padx=20, pady=20)

        close_btn = tk.Button(login_frame, text="Close", height=3, font=("Arial Bold", 14), width=10,
                              command=lambda: self.destroy(), fg='white', bg='#2c3e50', relief=tk.FLAT)
        close_btn.pack(pady=10)

        tk.Label(login_frame, text="Username:", font=("Arial Bold", 16), bg='#3498db',
                 fg='white').pack(side="top")
        username_entry = tk.Entry(login_frame, font=("Arial", 14))
        username_entry.pack(side="top", pady=5)

        tk.Label(login_frame, text="Password:", font=("Arial Bold", 16), bg='#3498db',
                 fg='white').pack(side="top")
        self.password_entry = tk.Entry(login_frame, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(login_frame, text="Show Password", variable=self.show_password_var,
                                             command=lambda: toggle_password(self))
        show_password_check.pack(side="top", pady=5)

        tk.Button(login_frame, text="Login", font=("Arial Bold", 14), width=15,
                  command=lambda: Client.login_check(username_entry, self.password_entry, self)).pack(pady=10)

        tk.Button(login_frame, text="You don't have an account? Click here!",
                  font=("Arial", max(12, int(14))), width=40,
                  command=lambda: RegisterFrame(self)).pack()

        self.mainloop()


class RegisterFrame(tk.Frame):
    def back_button(self, master):
        master.destroy()
        LoginWindow()

    def __init__(self, master):
        super().__init__(master, bg='#3498db')  # Set frame background color to blue
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        register_frame = tk.Frame(self, bg='#3498db')
        register_frame.pack(padx=20, pady=20)

        back_btn = tk.Button(register_frame, text="Back", height=3, font=("Arial Bold", 15), width=10,
                             command=lambda: self.back_button(master), fg='white', bg='#2c3e50')
        back_btn.pack(side="left", pady=10)

        close_btn = tk.Button(register_frame, text="Close", height=3, font=("Arial Bold", 15), width=10,
                              command=lambda: master.destroy(), fg='white', bg='#2c3e50')
        close_btn.pack(side="left", pady=10)

        lbl_username = tk.Label(self, text="Username:", font=("Arial Bold", 15), fg='white', bg='#3498db')
        lbl_username.pack(side="top", pady=5)

        username_entry = tk.Entry(self, font=("Arial", 15))
        username_entry.pack(side="top", pady=5)

        lbl_password = tk.Label(self, text="Password:", font=("Arial Bold", 15), fg='white', bg='#3498db')
        lbl_password.pack(side="top", pady=5)

        self.password_entry = tk.Entry(self, show="*", font=("Arial", 15))
        self.password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(self, text="Show Password", variable=self.show_password_var,
                                             command=lambda: toggle_password(self))
        show_password_check.pack(side="top", pady=5)

        lbl_type = tk.Label(self, text="User Type:", font=("Arial Bold", 15), fg='white', bg='#3498db')
        lbl_type.pack(side="top", pady=5)

        clicked = tk.StringVar()
        type_option = tk.OptionMenu(self, clicked, "Student", "Teacher", "Friend")
        type_option.configure(font=("Arial", 15), fg='white', bg='#3498db')
        type_option.pack(pady=5)

        btn_register = tk.Button(self, text="Register", font=("Arial Bold", 15), width=15,
                                 command=lambda: Client.registration_check(username_entry, self.password_entry, clicked, master),
                                 fg='white', bg='#3498db', relief=tk.RAISED)
        btn_register.pack(pady=10)

        self.lbl_num = tk.Label(self, text="Username Pattern: \n {Your ID}_{Your Nickname}", height=3, font=("Arial Bold", 20),
                                fg='white', bg='#3498db', wraplength=600)
        self.lbl_num.pack(side="top")

        self.lbl_num = tk.Label(self, text="Conditions for a strong password: \n"
                                           "*At least 1 symbol from &/!/#/@"
                                           "\n *At least 3 big letters & 3 small letters"
                                           "\n *At least 2 digits \n"
                                           "*At least 12 characters", height=8, font=("Arial Bold", 20),
                                fg='white', bg='#3498db', wraplength=600)
        self.lbl_num.pack(side="top")


class JoiningStudentFrame(tk.Frame):
    def __init__(self, master, student_username, num):
        super().__init__(master, bg='#3498db')
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        btn_click = tk.Button(self, text="Disconnect", height=3, font=("Arial Bold", 15), width=10,
                              command=lambda: Client.logout_button(student_username, master), fg='white',
                              bg='#3498db')  # Set foreground color to white, background color to blue
        btn_click.pack()

        if num == 0:
            self.lbl_num = tk.Label(self, text=f"Welcome {student_username}! \n Do you want to hide your account "
                                               f"while you are disconnected?", height=4, font=("Arial Bold", 20),
                                    fg='white', bg='#3498db', wraplength=600)
            self.lbl_num.pack(side="top")

            self.btn_click = tk.Button(self, text="YES", height=3, font=("Arial Bold", 15), width=10,
                                       command=lambda: Client.add_to_clients_messages(master, True, student_username),
                                       fg='white', bg='#3498db')  # Set foreground and background color
            self.btn_click.pack()

            self.btn_click1 = tk.Button(self, text="NO", height=3, font=("Arial Bold", 15), width=10,
                                        command=lambda: Client.add_to_clients_messages(master, False, student_username),
                                        fg='white', bg='#3498db')  # Set foreground and background color
            self.btn_click1.pack()

            lbl_num1 = tk.Label(self, text=f"After you choose, please wait until"
                                           f"\n the teacher connects with you or disconnect.", height=3,
                                font=("Arial Bold", 20), fg='white', bg='#3498db', wraplength=600)
            lbl_num1.pack(pady=10)

        elif num == 1:
            threading.Thread(target=Client.get_the_next_frame, args=(master, student_username, 0)).start()

            lbl_num = tk.Label(self, text=f"Thanks {student_username}! \n Please wait until the teacher"
                                          f" connects with you. \n"
                                          f" Meanwhile, if you chose NO, you can disconnect.", height=3,
                               font=("Arial Bold", 20), fg='white', bg='#3498db')
            lbl_num.pack(pady=30)

        elif num == 2:
            get_the_feedback_thread = threading.Thread(target=Client.get_the_next_frame, args=(master, student_username, 0))
            if not get_the_feedback_thread.is_alive():
                get_the_feedback_thread.start()

            btn_click = tk.Button(self, text="Instructions", height=3, font=("Arial Bold", 15), width=10,
                                  command=lambda: InstructionsForStudents(master, student_username, 0), fg='white',
                                  bg='#3498db')  # Set foreground color to white, background color to blue
            btn_click.pack()

            lbl_num = tk.Label(self, text=f"Thanks {student_username}! \n If you've completed your driving lessons, \n"
                                          f"Please disconnect. Otherwise, please wait until \n"
                                          f" another teacher connects with you.",
                               height=5, font=("Arial Bold", 20), fg='white', bg='#3498db', wraplength=800)
            lbl_num.pack(pady=30)


class TeacherOptionsFrame(tk.Frame):
    def __init__(self, master, teacher_username):
        super().__init__(master, bg='#3498db')  # Set frame background color to blue
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        # Frame for Disconnect and Refresh buttons
        btn_frame = tk.Frame(self, bg='#3498db')
        btn_frame.pack(side="top", pady=10)

        btn_disconnect = tk.Button(btn_frame, text="Disconnect", height=3, font=("Arial Bold", 15), width=10,
                                   command=lambda: Client.logout_button(teacher_username, master),
                                   fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_disconnect.pack(side="left", padx=10)  # Set side to "left" and add some padding

        btn_refresh = tk.Button(btn_frame, text="Refresh", height=3, font=("Arial Bold", 15), width=10,
                                command=lambda: TeacherOptionsFrame(master, teacher_username),
                                fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_refresh.pack(side="left", padx=10)  # Set side to "left" and add some padding

        if Client.passed_step2_in_registration(teacher_username) == "True":
            btn_back = tk.Button(btn_frame, text="Back", height=3, font=("Arial Bold", 15), width=10,
                                 command=lambda: TeacherFeedbacksFrame(master, teacher_username),
                                 fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
            btn_back.pack(side="left", padx=10)  # Set side to "left" and add some padding

        # Frame for the text
        text_frame = tk.Frame(self, bg='#3498db')
        text_frame.pack(side="top", pady=10)

        self.check = Client.list_of_students()

        if self.check:

            lbl_num = tk.Label(text_frame, text=f"Welcome {teacher_username}! \n"
                                                f" Please choose your student:", height=3, font=("Arial Bold", 20),
                                                fg='white', bg='#3498db')
            lbl_num.pack(side="top", pady=10)

            self.search_entry = ttk.Entry(self)
            self.search_entry.pack(side="top", pady=5)
            self.search_entry.bind('<KeyRelease>', lambda event: filter_listbox(self, self.check))

            self.listbox = tk.Listbox(self, width=30, height=10)
            self.listbox.pack(side="left", fill="both")

            for option in self.check:
                self.listbox.insert("end", option)

            enter_button = ttk.Button(self, text="Enter",
                                      command=lambda: Client.teacher_chose_student(master, teacher_username, self.listbox.curselection(), self.listbox))
            enter_button.pack(side="left", padx=10)

        else:
            lbl_no_students = tk.Label(text_frame, text=f"Sorry {teacher_username} \n"
                                                        f" There are no students ready to connect right now! "
                                                        f"\n Please refresh or try again later.", height=3, font=("Arial Bold", 20),
                                       fg='white', bg='#3498db')
            lbl_no_students.pack(side="top", pady=10)

class StudentFeedbacksFrame(tk.Frame):
    def __init__(self, master, student_username, num):
        super().__init__(master, bg='#3498db')  # Set frame background color to blue
        master.winfo_children()[0].destroy()
        self.pack(padx=50, pady=50)  # Increased padding for better spacing

        if num == 1:
            Client.ty()

        time.sleep(2)

        # Frame for Disconnect, Last Lesson, Share Friends, and Refresh buttons
        btn_frame = tk.Frame(self, bg='#3498db')
        btn_frame.pack(side="top", pady=20)

        btn_last_lesson = tk.Button(btn_frame, text="Last Lesson", height=3, font=("Arial Bold", 15), width=10,
                                    command=lambda: last_lesson_tool(student_username, self),
                                    fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_last_lesson.pack(side="left", padx=10)

        btn_last_lesson = tk.Button(btn_frame, text="Instructions", height=3, font=("Arial Bold", 15), width=10,
                                    command=lambda: InstructionsForStudents(master, student_username, 1),
                                    fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_last_lesson.pack(side="left", padx=10)

        btn_share_friends = tk.Button(btn_frame, text="  Share \n Friends", height=3, font=("Arial Bold", 15), width=10,
                                      command=lambda: StudentSharesWithFriendFrame(master, student_username),
                                      fg='white', bg='#3498db')
        btn_share_friends.pack(side="left", padx=10)

        btn_disconnect = tk.Button(btn_frame, text="Disconnect", height=3, font=("Arial Bold", 15), width=10,
                                   command=lambda: Client.logout_button(student_username, master),
                                   fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_disconnect.pack(side="left", padx=10)

        btn_refresh = tk.Button(btn_frame, text="Refresh", height=3, font=("Arial Bold", 15), width=10,
                                command=lambda: StudentFeedbacksFrame(master, student_username, 1),
                                fg='white', bg='#3498db')
        btn_refresh.pack(side="left", padx=10)

        lbl_num = tk.Label(self, text=f"Hello {student_username}!"
                                      f" Please choose the lesson \n number you want to get feedback on",
                           height=3, font=("Arial Bold", 20), fg='white', bg='#3498db')
        lbl_num.pack(side="top", pady=30)

        check = list(range(1, Client.how_much_lessons(master, student_username) + 1))
        self.chosen_lesson_number = tk.StringVar(self)
        type_option = tk.OptionMenu(self, self.chosen_lesson_number, *check)
        type_option.configure(font=("Arial", 14))  # Set font size for the option menu
        type_option.pack(side="top", pady=10)

        btn_enter = tk.Button(self, text="Enter", height=3, font=("Arial Bold", 15), width=10,
                              command=lambda: self.enter_button(master, student_username), fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_enter.pack(side="top", pady=10)

        self.feedback_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10)
        self.feedback_text.pack(side="top", pady=10)
        self.feedback_text.config(state="disabled")

        remove_student_thread = threading.Thread(target=Client.get_the_previous_frame, args=(master, student_username))
        remove_student_thread.start()

    def enter_button(self, master, student_username):
        Client.ty()
        self.feedback_text.config(state="normal")
        lesson_number = self.chosen_lesson_number.get()
        feedback_text_content = Client.feedbacks_per_lesson(master, student_username, lesson_number)
        threading.Thread(target=Client.get_the_previous_frame, args=(master, student_username)).start()
        self.feedback_text.insert(tk.END, feedback_text_content)
        self.feedback_text.config(state="disabled")


class TeacherFeedbacksFrame(tk.Frame):
    def variable_lesson_number(self, *args):
        student_username = self.student_username.get()
        options = list(range(1, Client.how_much_lessons(self.master, student_username) + 1))
        self.lesson_number.set("")
        self.type_option2["menu"].delete(0, "end")
        for option in options:
            self.type_option2["menu"].add_command(label=option,
                                                  command=lambda value=option: self.lesson_number.set(value))

    def __init__(self, master, teacher_username):
        self.master = master
        super().__init__(self.master, bg='#3498db')  # Set frame background color to blue
        self.master.winfo_children()[0].destroy()
        self.pack(padx=50, pady=50)  # Increased padding for better spacing

        # Frame for Disconnect, Add Student, Add Lesson, Last Lesson buttons
        btn_frame = tk.Frame(self, bg='#3498db')
        btn_frame.pack()

        btn_remove_student = tk.Button(btn_frame, text="  Remove \n Student", height=3, font=("Arial Bold", 15), width=10,
                                       command=lambda: Client.remove_student(self.master, teacher_username,
                                                                             self.student_username.get()),
                                       fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_remove_student.pack(side="left", padx=10)

        btn_add_student = tk.Button(btn_frame, text="Add Student", height=3, font=("Arial Bold", 15), width=10,
                                    command=lambda: TeacherOptionsFrame(self.master, teacher_username),
                                    fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_add_student.pack(side="left", padx=10)

        btn_add_lesson = tk.Button(btn_frame, text="Add Lesson", height=3, font=("Arial Bold", 15), width=10,
                                   command=lambda: Client.add_lesson(self, self.student_username.get(),
                                                                     teacher_username),
                                   fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_add_lesson.pack(side="left", padx=10)

        btn_last_lesson = tk.Button(btn_frame, text="Last Lesson", height=3, font=("Arial Bold", 15), width=10,
                                    command=lambda: last_lesson_tool(self.student_username.get(), self),
                                    fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_last_lesson.pack(side="left", padx=10)

        btn_disconnect = tk.Button(btn_frame, text="Disconnect", height=3, font=("Arial Bold", 15), width=10,
                                   command=lambda: Client.logout_button(teacher_username, self.master),
                                   fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_disconnect.pack(side="left", padx=10)

        lbl_num = tk.Label(self, text=f"Hello {teacher_username}! \n "
                                      f"Please choose your current student:", height=3, font=("Arial Bold", 20),
                           fg='white', bg='#3498db')
        lbl_num.pack(side="top", pady=10)

        check = Client.list_of_students_per_teacher(teacher_username)
        self.student_username = tk.StringVar(self)

        if check:
            self.type_option = tk.OptionMenu(self, self.student_username, *check)
        else:
            self.type_option = tk.OptionMenu(self, self.student_username, "")
            self.student_username.set("No Students Available")
            self.type_option.configure(state='disabled')
            messagebox.showinfo("A message", "You don't have students right now. Please add at least one to the system.")

        self.type_option.pack()
        self.student_username.trace_add("write", self.variable_lesson_number)

        lbl_num = tk.Label(self, text="Please choose the lesson number", height=3, font=("Arial Bold", 20),
                           fg='white', bg='#3498db')
        lbl_num.pack(side="top")

        self.lesson_number = tk.StringVar(self)
        self.type_option2 = tk.OptionMenu(self, self.lesson_number, "")
        self.type_option2.pack()

        lbl_num = tk.Label(self, text="Please enter your verbal & quantitative feedback", height=3,
                           font=("Arial Bold", 20), fg='white', bg='#3498db')
        lbl_num.pack(side="top")

        quantitative_feedback = tk.StringVar()
        one_to_ten = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        type_option = tk.OptionMenu(self, quantitative_feedback, *one_to_ten)
        type_option.pack()

        verbal_feedback = tk.Entry(self, font=("Arial", 14), bd=3, relief="groove", fg='#3498db', bg='white')
        verbal_feedback.pack(side="top", pady=10)

        btn_enter = tk.Button(self, text="Enter", height=3, font=("Arial Bold", 15), width=10,
                              command=lambda: Client.add_feedbacks(self.student_username.get(), self.lesson_number,
                                                                   verbal_feedback, quantitative_feedback),
                              fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_enter.pack()


class StudentSharesWithFriendFrame(tk.Frame):
    def __init__(self, master, student_username):
        super().__init__(master, bg='#3498db')  # Set frame background color to blue
        master.winfo_children()[0].destroy()
        self.pack(padx=50, pady=50)  # Increased padding for better spacing

        btn_frame = tk.Frame(self, bg='#3498db')
        btn_frame.pack()

        btn_refresh = tk.Button(btn_frame, text="Refresh", height=3, font=("Arial Bold", 15), width=10,
                                command=lambda: StudentSharesWithFriendFrame(master, student_username),
                                fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_refresh.pack(side="left", padx=10)

        btn_disconnect = tk.Button(btn_frame, text="Disconnect", height=3, font=("Arial Bold", 15), width=10,
                                   command=lambda: Client.logout_button(student_username, master),
                                   fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_disconnect.pack(side="left", padx=10)

        btn_back = tk.Button(btn_frame, text="Back", height=3, font=("Arial Bold", 15), width=10,
                             command=lambda: StudentFeedbacksFrame(master, student_username, 1),
                             fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        btn_back.pack(side="left", padx=10)

        Client.ty()
        self.check = Client.friends_list(master, student_username)
        threading.Thread(target=Client.get_the_previous_frame, args=(master, student_username)).start()

        if self.check:

            lbl_num = tk.Label(self, text=f"Please choose the friend username \n"
                                          f" & lesson number you want to \n share with him"
                                          , height=3, font=("Arial Bold", 20), fg='white', bg='#3498db')
            lbl_num.pack(side="top")

            self.search_entry = ttk.Entry(btn_frame)
            self.search_entry.pack(side="top", pady=5)
            self.search_entry.bind('<KeyRelease>', lambda event: filter_listbox(self, self.check))

            self.listbox = tk.Listbox(self, width=30, height=10)
            self.listbox.pack(side="left", fill="both")

            for option in self.check:
                self.listbox.insert("end", option)

            Client.ty()
            check = list(range(1, Client.how_much_lessons(master, student_username) + 1))
            threading.Thread(target=Client.get_the_previous_frame, args=(master, student_username)).start()
            lesson_number = tk.StringVar()
            lessons_menu = tk.OptionMenu(self, lesson_number, *check)
            lessons_menu.pack()

            btn_enter = tk.Button(self, text="Share", height=3, font=("Arial Black", 15), width=10,
                                  command=lambda: Client.share_feedback_with_friend(master, lesson_number.get(),
                                                                                    student_username,
                                                                                    self.listbox.curselection(), self.listbox),
                                  fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
            btn_enter.pack()

        else:
            lbl_num = tk.Label(self,
                               text=f"There are no connected friends right now. \n Please refresh or try again later."
                               , height=3, font=("Arial Bold", 20), fg='white', bg='#3498db')
            lbl_num.pack(side="top")


class FriendsGetTheFeedbackFrame(tk.Frame):
    def __init__(self, master, friend_username):
        super().__init__(master, bg='#3498db')  # Set frame background color to blue
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        btn_click = tk.Button(self, text="Disconnect", height=3, font=("Arial Bold", 15), width=10,
                              command=lambda: Client.logout_button(friend_username, master), fg='white',
                              bg='#3498db')  # Set foreground color to white, background color to blue
        btn_click.pack()

        lbl_num = tk.Label(self, text=f"Welcome {friend_username}! \n"
                                      f" Here is the information your friends decided \n to share with you:",
                                      height=5, font=("Arial Bold", 20), fg='white', bg='#3498db')
        lbl_num.pack(side="top", pady=10)

        self.feedback_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10)
        self.feedback_text.pack(side="top", pady=10)

        threading.Thread(target=Client.friend_gets_feedback, args=(self, friend_username)).start()

    def update_feedback_text(self, friend_username, text):
        self.feedback_text.config(state="normal")
        self.feedback_text.insert(tk.END, text)
        self.feedback_text.config(state="disabled")
        threading.Thread(target=Client.friend_gets_feedback, args=(self, friend_username)).start()
        Client.friend_gets_feedback(self, friend_username)


class InstructionsForStudents(tk.Frame):
    def __init__(self, master, student_username, num):
        super().__init__(master, bg='#3498db')  # Set frame background color to blue
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        disconnect_button = tk.Button(self, text="Disconnect", height=3, font=("Arial Bold", 15), width=10,
                                      command=lambda: Client.logout_button(student_username, master),
                                      fg='white', bg='#3498db')  # Set foreground color to white, background color to blue
        disconnect_button.pack(side="left", padx=10)

        if num == 1:
            back_friends = tk.Button(self, text="Back", height=3, font=("Arial Bold", 15), width=10,
                                    command=lambda: StudentFeedbacksFrame(master, student_username, 1),
                                          fg='white', bg='#3498db') ##if he gets here from StudentFeedbacksFrame
        else:
            back_friends = tk.Button(self, text="Back", height=3, font=("Arial Bold", 15), width=10,
                                    command=lambda: JoiningStudentFrame(master, student_username, 2),
                                          fg='white', bg='#3498db') ##if he gets here from JoiningStudentFrame
        back_friends.pack(side="left", padx=10)

        lbl_num = tk.Label(self, text="Here is all you need to know before you start driving independently!",
                           height=3, font=("Arial Bold", 20), fg='white', bg='#3498db')
        lbl_num.pack(side="top", pady=10)

        # Create a Text widget for purposes... lefaret
        self.feedback_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10)
        self.feedback_text.pack(side="top", pady=10)

        text = WebScraping.web_scraping_from_department_of_transportation()

        self.feedback_text.config(state="normal")
        self.feedback_text.insert(tk.END, text)
        self.feedback_text.config(state="disabled")


def toggle_password(self_para):
    if self_para.show_password_var.get():
        self_para.password_entry.config(show="")
    else:
        self_para.password_entry.config(show="*")


# Function to filter the Listbox based on the search entry
def filter_listbox(listbox, check, event=None):
    search_value = listbox.search_entry.get().lower()
    listbox.listbox.delete(0, "end")
    for option in check:
        if search_value in option.lower():
            listbox.listbox.insert("end", option)


def last_lesson_tool(student_username, master):
    if student_username == "":
        messagebox.showerror("Error", "Please choose a student")
    else:
        last_lesson = Client.last_lesson(student_username)

        if not hasattr(last_lesson_tool, 'frame_created'):
            frame = tk.Frame(master, bg='#3498db')
            frame.pack(padx=50, pady=50)

            lbl_num = tk.Label(frame, text=f"The last lesson you entered is: {last_lesson}", height=3,
                               font=("Arial Bold", 20), fg='white', bg='#3498db')
            lbl_num.pack(side="top", pady=10)

            last_lesson_tool.frame_created = True

        else:
            lbl_num = master.winfo_children()[7]
            lbl_num.config(text=f"The last lesson is: {last_lesson}")
