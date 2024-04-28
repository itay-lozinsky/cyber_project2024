import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from tkinter import ttk
import WebScraping
from Client import user_management, student_management, teacher_management


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login Window")
        self.geometry("700x750")
        self.configure(bg="#36393f")

        login_frame = tk.Frame(self, bg='#36393f')
        login_frame.pack(padx=20, pady=20)

        button_frame = tk.Frame(login_frame, bg='#36393f')
        button_frame.pack(pady=10)

        close_btn = tk.Button(button_frame, text="Close", height=3, font=("Helvetica", 16), width=10,
                              command=lambda: self.destroy(), fg='white', bg='#7289da')
        close_btn.pack(side="left", padx=5)

        content_frame = tk.Frame(login_frame, bg='#36393f')
        content_frame.pack(padx=20, pady=(20, 40), expand=True, fill=tk.BOTH)  # Increased bottom padding

        username_label = tk.Label(content_frame, text="Username:", font=("Helvetica", 16, "bold"), fg='white', bg='#36393f')
        username_label.pack(side="top", pady=10)

        username_entry = tk.Entry(content_frame, font=("Helvetica", 16))
        username_entry.pack(side="top", pady=5, fill=tk.X)

        password_label = tk.Label(content_frame, text="Password:", font=("Helvetica", 16, "bold"), fg='white', bg='#36393f')
        password_label.pack(side="top", pady=10)

        self.password_entry = tk.Entry(content_frame, show="*", font=("Helvetica", 16))
        self.password_entry.pack(side="top", pady=5, fill=tk.X)

        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(content_frame, text="Show Password", variable=self.show_password_var,
                                             command=lambda: toggle_password(self), fg='white', bg='#36393f', font=("Helvetica", 14), selectcolor='black')
        show_password_check.pack(side="top", pady=5)

        login_btn = tk.Button(content_frame, text="Login", font=("Helvetica", 16), width=15,
                              command=lambda: user_management.login_check(username_entry, self.password_entry, self),
                              fg='white', bg='#7289da', relief=tk.RAISED, cursor="hand2")
        login_btn.pack(side="top", pady=20)

        separator = ttk.Separator(content_frame, orient='horizontal')
        separator.pack(side="top", fill=tk.X, pady=(20, 30))

        register_btn = tk.Button(content_frame, text="You don't have an account? Click here!",
                                 command=lambda: RegisterFrame(self), font=("Helvetica", 18, "bold"), fg='white', bg='#7289da', relief=tk.RAISED)
        register_btn.pack(side="top", pady=20)  # Increased top padding for the button

        self.mainloop()


class RegisterFrame(tk.Frame):
    def back_button(self, master):
        master.destroy()
        LoginWindow()

    def __init__(self, master):
        super().__init__(master, bg='#36393f')
        master.geometry("700x1000")  # Set the geometry of the master window
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        register_frame = tk.Frame(self, bg='#36393f')
        register_frame.pack(padx=20, pady=20)

        button_frame = tk.Frame(register_frame, bg='#36393f')
        button_frame.pack(pady=10)

        back_btn = tk.Button(button_frame, text="Back", height=3, font=("Helvetica", 16), width=10,
                             command=lambda: self.back_button(master), fg='white', bg='#7289da')
        back_btn.pack(side="left", padx=5)

        close_btn = tk.Button(button_frame, text="Close", height=3, font=("Helvetica", 16), width=10,
                              command=lambda: master.destroy(), fg='white', bg='#7289da')
        close_btn.pack(side="left", padx=5)

        content_frame = tk.Frame(register_frame, bg='#36393f')
        content_frame.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)

        lbl_username = tk.Label(content_frame, text="Username:", font=("Helvetica", 16, "bold"), fg='white', bg='#36393f')
        lbl_username.pack(side="top", pady=10)

        username_entry = tk.Entry(content_frame, font=("Helvetica", 16))
        username_entry.pack(side="top", pady=5, fill=tk.X)

        lbl_password = tk.Label(content_frame, text="Password:", font=("Helvetica", 16, "bold"), fg='white', bg='#36393f')
        lbl_password.pack(side="top", pady=10)

        self.password_entry = tk.Entry(content_frame, show="*", font=("Helvetica", 16))
        self.password_entry.pack(side="top", pady=5, fill=tk.X)

        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(content_frame, text="Show Password", variable=self.show_password_var,
                                             command=lambda: toggle_password(self), fg='white', bg='#36393f', font=("Helvetica", 14), selectcolor='black')
        show_password_check.pack(side="top", pady=5)

        lbl_type = tk.Label(content_frame, text="User Type:", font=("Helvetica", 16, "bold"), fg='white', bg='#36393f')
        lbl_type.pack(side="top", pady=10)

        clicked = tk.StringVar()
        type_option = tk.OptionMenu(content_frame, clicked, "Student", "Teacher", "Friend")
        type_option.configure(font=("Helvetica", 16), fg='white', bg='#36393f')
        type_option.pack(side="top", pady=5, fill=tk.X)

        btn_register = tk.Button(content_frame, text="Register", font=("Helvetica", 16), width=15,
                                 command=lambda: user_management.registration_check(username_entry, self.password_entry, clicked, master),
                                 fg='white', bg='#7289da', relief=tk.RAISED)
        btn_register.pack(side="top", pady=20)

        separator = ttk.Separator(content_frame, orient='horizontal')
        separator.pack(side="top", fill=tk.X, pady=10)

        conditions_frame = tk.Frame(content_frame, bg='#36393f')
        conditions_frame.pack(side="top", pady=(20, 35), fill=tk.BOTH, expand=True)

        self.lbl_num = tk.Label(conditions_frame, text="Username Pattern:", font=("Helvetica", 18, "bold"),
                                       fg='white', bg='#36393f')
        self.lbl_num.pack(side="top", pady=20)

        self.lbl_num = tk.Label(conditions_frame, text="{Your ID}_{Your Nickname}", font=("Helvetica", 18),
                                fg='white', bg='#36393f')
        self.lbl_num.pack(side="top", pady=6)

        self.lbl_conditions = tk.Label(conditions_frame, text="Conditions for a strong password:", font=("Helvetica", 18, "bold"),
                                       fg='white', bg='#36393f', wraplength=600)
        self.lbl_conditions.pack(side="top", pady=12)

        conditions = "*At least 3 big letters & 3 small letters & 2 digits\n*At least one symbol from %, !, # or @\n*At least 12 characters"

        self.lbl_conditions_text = tk.Label(conditions_frame, text=conditions,
                                            font=("Helvetica", 17), fg='white', bg='#36393f')
        self.lbl_conditions_text.pack(side="top")


class JoiningStudentFrame(tk.Frame):
    def __init__(self, master, student_username, num):
        super().__init__(master, bg='#36393f')
        master.geometry("700x600")
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        logout_button = tk.Button(self, text="Logout", height=3, font=("Helvetica", 16), width=10,
                                   command=lambda: user_management.logout_button(student_username, master),
                                   fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        logout_button.pack(padx=5)

        if num == 0:
            self.lbl_num = tk.Label(self, text=f"Welcome {student_username[10:]}! \n Do you want to hide your account "
                                               f"while you are disconnected?", height=4, font=("Helvetica", 20, "bold"),
                                    fg='white', bg='#36393f', wraplength=600)
            self.lbl_num.pack(side="top")

            self.btn_click = tk.Button(self, text="YES", height=3, font=("Helvetica", 15, "bold"), width=10,
                                       command=lambda: student_management.add_students_to_yes_or_no_table(master, True, student_username),
                                       fg='white', bg='#7289da')
            self.btn_click.pack()

            self.btn_click1 = tk.Button(self, text="NO", height=3, font=("Helvetica", 15, "bold"), width=10,
                                        command=lambda: student_management.add_students_to_yes_or_no_table(master, False, student_username),
                                        fg='white', bg='#7289da')
            self.btn_click1.pack()

            lbl_num1 = tk.Label(self, text=f"After you choose, please wait until"
                                           f"\n the teacher connects with you or logout.", height=3,
                                font=("Helvetica", 20), fg='white', bg='#36393f', wraplength=600)
            lbl_num1.pack(pady=10)

        elif num == 1:
            threading.Thread(target=student_management.get_the_next_frame, args=(master, student_username)).start()

            lbl_num = tk.Label(self, text=f"Thanks {student_username[10:]}! \n Please wait until the teacher"
                                          f" connects with you. \n"
                                          f" Meanwhile, if you chose NO, you can logout.", height=3,
                               font=("Helvetica", 20, "bold"), fg='white', bg='#36393f')
            lbl_num.pack(pady=30)

        elif num == 2:
            get_the_feedback_thread = threading.Thread(target=student_management.get_the_next_frame, args=(master, student_username))
            if not get_the_feedback_thread.is_alive():
                get_the_feedback_thread.start()

            btn_click = tk.Button(self, text="Instructions", height=3, font=("Helvetica", 15), width=10,
                                  command=lambda: InstructionsForStudents(master, student_username, 0), fg='white',
                                  bg='#7289da')
            btn_click.pack()

            lbl_num = tk.Label(self, text=f"Thanks {student_username[10:]}! \n If you've completed your driving lessons, \n"
                                          f"Please disconnect. Otherwise, please wait until \n"
                                          f" another teacher connects with you.",
                               height=5, font=("Helvetica", 20, "bold"), fg='white', bg='#36393f', wraplength=800)
            lbl_num.pack(pady=30)


class TeacherOptionsFrame(tk.Frame):
    def __init__(self, master, teacher_username):
        super().__init__(master, bg='#36393f')  # Set frame background color to dark grey
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        # Frame for Disconnect and Refresh buttons
        btn_frame = tk.Frame(self, bg='#36393f')
        btn_frame.pack(side="top", pady=10)

        logout_button = tk.Button(btn_frame, text="Logout", height=3, font=("Helvetica", 16), width=10,
                                   command=lambda: user_management.logout_button(teacher_username, master),
                                   fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        logout_button.pack(side="left", padx=5)

        btn_refresh = tk.Button(btn_frame, text="Refresh", height=3, font=("Helvetica", 16), width=10,
                                command=lambda: TeacherOptionsFrame(master, teacher_username),
                                fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        btn_refresh.pack(side="left", padx=5)

        if student_management.passed_stage_number2(teacher_username) == "True":
            btn_back = tk.Button(btn_frame, text="Back", height=3, font=("Helvetica", 16), width=10,
                                 command=lambda: TeacherFeedbacksFrame(master, teacher_username),
                                 fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
            btn_back.pack(side="left", padx=5)

        # Frame for the text
        text_frame = tk.Frame(self, bg='#36393f')
        text_frame.pack(side="top", pady=10)

        self.check = teacher_management.list_of_students()

        if self.check:
            master.geometry("700x1000")
            lbl_num = tk.Label(text_frame, text=f"Welcome {teacher_username[10:]}!\nPlease choose your student:", height=3, font=("Helvetica", 20, "bold"),
                                                fg='white', bg='#36393f')
            lbl_num.pack(side="top", pady=10)

            self.search_entry = tk.Entry(self, font=("Helvetica", 16))
            self.search_entry.pack(side="top", pady=5)
            self.search_entry.bind('<KeyRelease>', lambda event: filter_listbox(self, self.check))

            self.listbox = tk.Listbox(self, width=40, height=10, font=("Helvetica", 16))
            self.listbox.pack(fill="both", pady=(20, 30))

            for option in self.check:
                self.listbox.insert("end", option)

            enter_button = tk.Button(self, text="Enter", font=("Helvetica", 16), width=20,
                                      command=lambda: teacher_management.teacher_connecting_student(master, teacher_username, self.listbox), fg='white', bg='#7289da', relief=tk.RAISED, cursor="hand2")
            enter_button.pack(padx=30)

        else:
            master.geometry("700x600")
            lbl_no_students = tk.Label(text_frame, text=f"Sorry {teacher_username[10:]}!\nThere are no students ready to connect right now!\nPlease refresh or try again later.", height=3, font=("Helvetica", 18, "bold"),
                                       fg='white', bg='#36393f')
            lbl_no_students.pack(side="top", pady=10)


class TeacherFeedbacksFrame(tk.Frame):
    def on_listbox_select(self, event):
        selected_index = event.widget.curselection()
        if selected_index:
            selected_student = event.widget.get(selected_index[0])
            self.variable_lesson_number(selected_student)

    def variable_lesson_number(self, student_username):
        options = list(range(1, teacher_management.how_much_lessons(self.master, student_username) + 1))
        self.lesson_number.set("")
        self.type_option2["menu"].delete(0, "end")
        for option in options:
            self.type_option2["menu"].add_command(label=option,
                                                  command=lambda value=option: self.lesson_number.set(value))

    def variable_feedback_data(self, student_username):
        student_management.feedbacks_per_lesson(master, student_username, lesson_number)

    def last_entered_lesson_tool(self):
        if not self.listbox.curselection():
            messagebox.showerror("Error", "Please choose a student.")
            return
        student_username = self.listbox.get(self.listbox.curselection()[0])
        last_entered_lesson = teacher_management.last_entered_lesson(student_username)
        self.lbl_lesson.config(text=last_entered_lesson)

    def __init__(self, master, teacher_username):
        super().__init__(master, bg='#36393f')
        master.geometry("1200x800")  # Set the geometry of the master window
        self.master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20, fill="both", expand=True)  # Expand both horizontally and vertically

        # Frame for Disconnect, Add Student, Add Lesson, Last Lesson buttons
        btn_frame = tk.Frame(self, bg='#36393f')
        btn_frame.pack(fill="x", pady=10)  # Pack the button frame horizontally with padding

        btn_options = [
            ("Logout", lambda: user_management.logout_button(teacher_username, master)),
            ("Remove Student", lambda: teacher_management.remove_student(master, teacher_username, self.listbox)),
            ("Add Student", lambda: TeacherOptionsFrame(master, teacher_username)),
            ("Add Lesson", lambda: teacher_management.add_lesson(self, teacher_username, self.listbox)),
            ("Last Entered Lesson", lambda: self.last_entered_lesson_tool())
        ]

        for text, command in btn_options:
            btn = tk.Button(btn_frame, text=text, height=2, font=("Helvetica", 14), width=15,
                            command=command, fg='white', bg='#7289da', relief='raised', borderwidth=1)
            btn.pack(side="left", padx=5, fill="x", expand=True)

        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', pady=10)

        # Left Frame for Listbox
        left_frame = tk.Frame(self, bg='#36393f')
        left_frame.pack(side="left", padx=20, fill="both", expand=True)

        lbl_num = tk.Label(left_frame, text=f"Hello {teacher_username[10:]}!\nPlease choose your current student:",
                           height=2, font=("Helvetica", 18, "bold"), fg='white', bg='#36393f')
        lbl_num.pack(side="top", pady=10)

        self.search_entry = tk.Entry(left_frame, font=("Helvetica", 16), relief='sunken', borderwidth=2)
        self.search_entry.pack(side="top", pady=5)
        self.search_entry.bind('<KeyRelease>', lambda event: filter_listbox(self, check))

        self.listbox = tk.Listbox(left_frame, width=30, height=18, font=("Helvetica", 16), relief='sunken', borderwidth=2)
        self.listbox.pack(fill="both", pady=10)

        self.lbl_lesson = tk.Label(left_frame, text=f"Click on the 'Last Entered Lesson' button", height=2,
                              font=("Helvetica", 18, "bold"), fg='white', bg='#36393f')
        self.lbl_lesson.pack(side="top", pady=8)

        check = teacher_management.list_of_students_per_teacher(teacher_username)

        if check:
            for option in check:
                self.listbox.insert("end", option)

        else:
            self.listbox.insert("end", "No Students Available")
            self.listbox.configure(state='disabled')
            messagebox.showinfo("Message", "You don't have any students right now.\nPlease connect at least one.")

        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side="left", fill="y", padx=20)

        # Right Frame for Other Widgets and Buttons
        right_frame = tk.Frame(self, bg='#36393f')
        right_frame.pack(side="left", padx=20, fill="both", expand=True)

        lbl_num = tk.Label(right_frame, text="Please choose the lesson number", height=2,
                           font=("Helvetica", 18, "bold"), fg='white', bg='#36393f')
        lbl_num.pack(side="top", pady=10)

        self.lesson_number = tk.StringVar(right_frame)
        self.type_option2 = tk.OptionMenu(right_frame, self.lesson_number, "")
        self.type_option2.pack(pady=10, fill="x")

        lbl_num = tk.Label(right_frame, text="Please enter your verbal & quantitative feedback", height=2,
                           font=("Helvetica", 18, "bold"), fg='white', bg='#36393f')
        lbl_num.pack(side="top", pady=10)

        selected_value = tk.IntVar()
        selected_value.set(1)

        scale = tk.Scale(right_frame, from_=1, to=10, orient="horizontal", length=300,
                         variable=selected_value, fg="orange", troughcolor='#eb6134', borderwidth=2, relief='raised',
                         highlightthickness=0, sliderrelief="flat", bg='#36393f')
        scale.pack(padx=20, pady=20, fill="both", expand=True)

        verbal_feedback = scrolledtext.ScrolledText(right_frame, font=("Helvetica", 16), height=5, bd=2, relief="sunken", fg='#36393f', bg='white')
        verbal_feedback.pack(side="top", pady=10, fill="both", expand=True)

        btn_enter = tk.Button(right_frame, text="Share Feedback", height=2, font=("Helvetica", 16), width=20, relief='raised', borderwidth=1, cursor="hand2",
                              command=lambda: teacher_management.add_feedback(self.lesson_number,
                                                                              verbal_feedback, selected_value, self.listbox),
                              fg='white', bg='#7289da')
        btn_enter.pack(pady=10, fill="x")


class StudentFeedbacksFrame(tk.Frame):
    def last_entered_lesson_tool(self):
        if self.student_username == "":
            messagebox.showerror("Error", "Please choose a student.")
        else:
            last_entered_lesson = teacher_management.last_entered_lesson(self.student_username)
            self.lbl_lesson.config(text=last_entered_lesson)

    def __init__(self, master, student_username, num):
        super().__init__(master, bg='#36393f')
        self.student_username = student_username
        master.geometry("700x650")  # Set the geometry of the master window
        master.winfo_children()[0].destroy()
        self.pack(fill="both", expand=True, padx=20, pady=20)  # Expand both horizontally and vertically

        if num == 1:
            student_management.stopping_the_removing_thread()

        time.sleep(2)

        btn_frame_top = tk.Frame(self, bg='#36393f')  # Frame for top row of buttons
        btn_frame_top.pack(pady=10, fill="x")

        btn_frame_bottom = tk.Frame(self, bg='#36393f')  # Frame for bottom row of buttons
        btn_frame_bottom.pack(pady=10, fill="x")

        self.lbl_lesson = tk.Label(self, text=f"Click on the 'Last Lesson Entered' button",
                                   height=2, font=("Helvetica", 16, "bold"), fg='white', bg='#36393f')
        self.lbl_lesson.pack(side="top", pady=10)

        btn_options_top = [
            ("Logout", lambda: user_management.logout_button(self.student_username, master)),
            ("Refresh", lambda: StudentFeedbacksFrame(master, self.student_username, 1)),
            ("Share Friends", lambda: StudentSharesWithFriendFrame(master, self.student_username))
        ]

        btn_options_bottom = [
            ("Instructions", lambda: InstructionsForStudents(master, self.student_username, 1)),
            ("Last Entered Lesson", lambda: self.last_entered_lesson_tool())
        ]

        for text, command in btn_options_top:
            btn = tk.Button(btn_frame_top, text=text, height=2, font=("Helvetica", 14), width=15,
                            command=command, fg='white', bg='#7289da', relief='raised', borderwidth=1)
            btn.pack(side="left", padx=5, fill="x", expand=True)

        for text, command in btn_options_bottom:
            btn = tk.Button(btn_frame_bottom, text=text, height=2, font=("Helvetica", 14), width=15,
                            command=command, fg='white', bg='#7289da', relief='raised', borderwidth=1)
            btn.pack(side="left", padx=5, fill="x", expand=True)

        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', pady=10)

        lbl_num = tk.Label(self, text=f"Hello {self.student_username[10:]}!\nPlease choose the lesson number you want to get feedback on",
                           height=3, font=("Helvetica", 16, "bold"), fg='white', bg='#36393f')
        lbl_num.pack(side="top", pady=10)

        check = list(range(1, teacher_management.how_much_lessons(master, self.student_username) + 1))
        self.chosen_lesson_number = tk.StringVar(self)
        type_option = tk.OptionMenu(self, self.chosen_lesson_number, *check)
        type_option.pack(side="top", pady=10, fill="x")

        btn_enter = tk.Button(self, text="Enter", height=2, font=("Helvetica", 16), width=12,
                              command=lambda: self.enter_button(master), fg='white', bg='#7289da', relief='raised', borderwidth=1)
        btn_enter.pack(side="top", pady=10)

        feedback_frame = tk.Frame(self, bg='#36393f')
        feedback_frame.pack(side="top", pady=10, fill="both", expand=True)

        self.feedback_text = scrolledtext.ScrolledText(feedback_frame, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 14), relief='sunken', borderwidth=2)
        self.feedback_text.pack(side="top", pady=10, fill="both", expand=True)
        self.feedback_text.config(state="disabled")

        remove_student_thread = threading.Thread(target=student_management.get_the_previous_frame, args=(master, self.student_username))
        remove_student_thread.start()

    def enter_button(self, master):
        student_management.stopping_the_removing_thread()
        self.feedback_text.config(state="normal")
        lesson_number = self.chosen_lesson_number.get()
        feedback_text_content = student_management.feedbacks_per_lesson(master, self.student_username, lesson_number)
        threading.Thread(target=student_management.get_the_previous_frame, args=(master, self.student_username)).start()
        self.feedback_text.insert(tk.END, feedback_text_content)
        self.feedback_text.config(state="disabled")


class StudentSharesWithFriendFrame(tk.Frame):
    def __init__(self, master, student_username):
        super().__init__(master, bg='#36393f')  # Set frame background color to dark grey
        master.winfo_children()[0].destroy()
        self.pack(padx=50, pady=50)  # Increased padding for better spacing

        btn_frame = tk.Frame(self, bg='#36393f')
        btn_frame.pack()

        logout_button = tk.Button(btn_frame, text="Logout", height=3, font=("Helvetica", 16), width=12,
                                   command=lambda: user_management.logout_button(student_username, master),
                                   fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        logout_button.pack(side="left", padx=10)

        btn_refresh = tk.Button(btn_frame, text="Refresh", height=3, font=("Helvetica", 16), width=12,
                                command=lambda: StudentSharesWithFriendFrame(master, student_username),
                                fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        btn_refresh.pack(side="left", padx=10)

        btn_back = tk.Button(btn_frame, text="Back", height=3, font=("Helvetica", 16), width=12,
                             command=lambda: StudentFeedbacksFrame(master, student_username, 1),
                             fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        btn_back.pack(side="left", padx=10)

        student_management.stopping_the_removing_thread()
        self.check = student_management.list_of_connected_friends(master, student_username)
        threading.Thread(target=student_management.get_the_previous_frame, args=(master, student_username)).start()

        if self.check:
            lbl_num = tk.Label(self, text=f"Please choose the friend username & lesson number you want to share with him",
                               height=3, font=("Helvetica", 18, "bold"), fg='white', bg='#36393f')
            lbl_num.pack(side="top")

            self.search_entry = tk.Entry(btn_frame)
            self.search_entry.pack(side="top", pady=5)
            self.search_entry.bind('<KeyRelease>', lambda event: filter_listbox(self, self.check))

            self.listbox = tk.Listbox(self, width=30, height=10)
            self.listbox.pack(fill="both")

            for option in self.check:
                self.listbox.insert("end", option)

            student_management.stopping_the_removing_thread()
            check = list(range(1, teacher_management.how_much_lessons(master, student_username) + 1))
            threading.Thread(target=student_management.get_the_previous_frame, args=(master, student_username)).start()
            lesson_number = tk.StringVar()
            lessons_menu = tk.OptionMenu(self, lesson_number, *check)
            lessons_menu.pack()

            btn_enter = tk.Button(self, text="Share Feedback", height=3, font=("Helvetica", 16), width=12,
                                  command=lambda: student_management.share_feedback_with_friend(master, lesson_number.get(),
                                                                                        student_username, self.listbox),
                                  fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
            btn_enter.pack()

        else:
            lbl_num = tk.Label(self, text=f"There are no connected friends right now. \n Please refresh or try again later.",
                               height=3, font=("Helvetica", 18, "bold"), fg='white', bg='#36393f')
            lbl_num.pack(side="top")


class FriendsGetTheFeedbackFrame(tk.Frame):
    def __init__(self, master, friend_username):
        super().__init__(master, bg='#36393f')  # Set frame background color to dark grey
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        logout_button = tk.Button(self, text="Logout", height=3, font=("Helvetica", 16), width=10,
                              command=lambda: user_management.logout_button(friend_username, master), fg='white',
                              bg='#7289da')  # Set foreground color to white, button color to purple
        logout_button.pack()

        lbl_num = tk.Label(self, text=f"Welcome {friend_username[10:]}! \n"
                                      f"Here is the information your friends decided \n to share with you:",
                                      height=5, font=("Helvetica", 18, "bold"), fg='white', bg='#36393f')
        lbl_num.pack(side="top", pady=10)

        self.feedback_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10, bg='#7289da',
                                                       fg='white', font=("Helvetica", 14))
        self.feedback_text.pack(side="top", pady=10)

        threading.Thread(target=user_management.friend_gets_feedback, args=(self, friend_username)).start()

    def update_feedback_text(self, friend_username, text):
        self.feedback_text.config(state="normal")
        self.feedback_text.insert(tk.END, text)
        self.feedback_text.config(state="disabled")
        threading.Thread(target=user_management.friend_gets_feedback, args=(self, friend_username)).start()


class InstructionsForStudents(tk.Frame):
    def __init__(self, master, student_username, num):
        super().__init__(master, bg='#36393f')  # Set frame background color to dark grey
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)

        logout_button = tk.Button(self, text="Logout", height=3, font=("Helvetica", 16), width=10,
                                  command=lambda: user_management.logout_button(student_username, master),
                                  fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        logout_button.pack(side="left", padx=10)

        if num == 1:
            back_button = tk.Button(self, text="Back", height=3, font=("Helvetica", 16), width=10,
                                    command=lambda: StudentFeedbacksFrame(master, student_username, 1),
                                    fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        else:
            back_button = tk.Button(self, text="Back", height=3, font=("Helvetica", 16), width=10,
                                    command=lambda: JoiningStudentFrame(master, student_username, 2),
                                    fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        back_button.pack(side="left", padx=10)

        back1_button = tk.Button(self, text="Quiz", height=3, font=("Helvetica", 16), width=10,
                                command=lambda: QuizApp(master),
                                fg='white', bg='#7289da')  # Set foreground color to white, button color to purple
        back1_button.pack(side="left", padx=10)

        lbl_num = tk.Label(self, text="Here is all you need to know before you start driving independently!",
                           height=3, font=("Helvetica", 18, "bold"), fg='white', bg='#36393f')
        lbl_num.pack(side="top", pady=10)

        # Create a Text widget for displaying instructions
        self.feedback_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10, bg='#7289da',
                                                       fg='white', font=("Helvetica", 14))
        self.feedback_text.pack(side="top", pady=10)

        # Web scraping for instructions from the Department of Transportation
        text = WebScraping.webscraping_from_department_of_transportation()

        self.feedback_text.config(state="normal")
        self.feedback_text.insert(tk.END, text)
        self.feedback_text.config(state="disabled")


class QuizApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='#36393f')  # Set frame background color to dark grey
        master.winfo_children()[0].destroy()
        self.pack(padx=20, pady=20)
        self.master = master

        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "answer": "Paris"
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "answer": "4"
            }
        ]
        self.current_question = 0
        self.score = 0

        self.question_label = tk.Label(self.master, text="", font=("Helvetica", 14))
        self.question_label.pack(pady=20)

        self.radio_var = tk.StringVar()
        for i in range(4):
            option = tk.Radiobutton(self.master, text="", variable=self.radio_var, value="")
            option.pack(anchor="w")

        self.next_button = tk.Button(self.master, text="Next", command=self.next_question)
        self.next_button.pack(pady=20)

        self.display_question()

    def display_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data["question"])

            for i, option in enumerate(question_data["options"]):
                self.master.nametowidget(f".!radiobutton{i}").config(text=option, value=option)

    def next_question(self):
        selected_answer = self.radio_var.get()
        correct_answer = self.questions[self.current_question]["answer"]

        if selected_answer == correct_answer:
            self.score += 1

        self.current_question += 1
        self.radio_var.set("")  # Reset radio button selection

        if self.current_question < len(self.questions):
            self.display_question()
        else:
            self.show_result()

    def show_result(self):
        self.question_label.config(text=f"Quiz completed!\nYour score: {self.score}/{len(self.questions)}")
        self.next_button.config(text="Restart", command=self.restart_quiz)

    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        self.display_question()
        self.next_button.config(text="Next", command=self.next_question)


def toggle_password(self_para):
    if self_para.show_password_var.get():
        self_para.password_entry.config(show="")
    else:
        self_para.password_entry.config(show="*")


# Function to filter the Listbox based on the search entry
def filter_listbox(listbox, check):
    search_value = listbox.search_entry.get().lower()
    listbox.listbox.delete(0, "end")
    for option in check:
        if search_value in option.lower():
            listbox.listbox.insert("end", option)
