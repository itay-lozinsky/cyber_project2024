from DBhandle import users_db, feedbacks_db, waiting_students_db
import Encryption
import threading
import Objects
import socket
import pickle


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object using IPv4 and TCP protocol
server_socket.bind(('127.0.0.1', 4444))  # Bind the socket to a specific IP address and port
server_socket.listen()  # Start listening for incoming connections


connected_users = {}  # Dictionary to keep track of connected users


def handle_client(client_obj):
    """
    :param client_obj: The client socket object representing the connection with a client.
    Handles requests and interactions for a connected client.

    This function runs in a loop to continuously listen for incoming messages from the client object.
    It decodes the received data, splits it based on a '*', and processes each request
    or command from the client.
    """
    while True:
        data = client_obj.recv(1024).decode().split('*')
        if not data:
            break
        # Process client requests based on the received data
        # Add your code here to handle different types of requests from the client

        # Users Table

        if data[0] == Objects.Enum.REGISTRATION:
            username = data[1]
            password = data[2]
            user_type = data[3]
            answer = users_db.registration_process(username, Encryption.encrypted_password(password), user_type)
            if answer in ["Student", "Teacher", "Friend"]:
                connected_users[username] = client_obj  # If valid, adds the users to the dictionary
            client_obj.send(answer.encode())

        elif data[0] == Objects.Enum.LOGINING:
            username = data[1]
            password = data[2]
            answer = users_db.login_process(username, Encryption.encrypted_password(password))
            if answer in ["Student", "Teacher", "Friend"]:
                connected_users[username] = client_obj  # If valid, adds the users to the dictionary
            client_obj.send(answer.encode())

        elif data[0] == Objects.Enum.CONNECTED_FRIENDS_LIST:
            answer = users_db.friends_list()
            answer = [e for e in connected_users.keys() if e in answer]  # Removes all the disconnect friends
            client_obj.send(pickle.dumps(answer))

        # WaitingStudents Table

        elif data[0] == Objects.Enum.YES:
            student_username = data[1]
            waiting_students_db.add_student("YES", student_username)
        elif data[0] == Objects.Enum.NO:
            student_username = data[1]
            waiting_students_db.add_student("NO", student_username)

        elif data[0] == Objects.Enum.STAGE1:
            student_username = data[1]
            answer = waiting_students_db.stage_number1(student_username)
            client_obj.send(answer.encode())

        elif data[0] == Objects.Enum.STUDENT_LIST:
            list1 = waiting_students_db.list_of_students(1)  # List of students who chose "YES"
            list2 = waiting_students_db.list_of_students(2)  # List of students who chose "NO"
            list3 = waiting_students_db.list_of_students(3)  # List of students already connected by their teacher
            upgraded_list1 = [e for e in connected_users.keys() if e in list1]
            # Removes "YES" students currently disconnected
            untied_list = upgraded_list1 + list2  # Combine "YES" and connected students with all "NO" students
            final_list = [e for e in untied_list if
                          e not in list3 and e is not None]  # Remove students already connected by their teacher
            client_obj.send(pickle.dumps(final_list))

        # Feedbacks Table

        elif data[0] == Objects.Enum.STAGE2:
            username = data[1]
            answer = feedbacks_db.stage_number2(username)
            client_obj.send(answer.encode())

        elif data[0] == Objects.Enum.THE_NEXT_FRAME:
            student_username = data[1]
            teacher_username = data[2]
            if student_username in connected_users.keys():
                connected_users[student_username].send("The Next Frame".encode())
                # The thread activated on "the_next_frame" func will get this message and navigates the student onward
            feedbacks_db.add_users_to_feedbacks(student_username, teacher_username)  # Adds student to feedbacks table

        elif data[0] == Objects.Enum.LIST_STUDENTS_PER_TEACHER:
            teacher_username = data[1]
            answer = feedbacks_db.list_of_students_per_teacher(teacher_username)
            client_obj.send(pickle.dumps(answer))

        elif data[0] == Objects.Enum.HOW_MUCH_LESSONS:
            student_username = data[1]
            answer = feedbacks_db.how_much_lessons(student_username)
            client_obj.send(answer.encode())

        elif data[0] == Objects.Enum.ADD_LESSON:
            student_username = data[1]
            teacher_username = data[2]
            feedbacks_db.add_lesson(student_username, teacher_username)

        elif data[0] == Objects.Enum.LAST_ENTERED_LESSON:
            student_username = data[1]
            answer = feedbacks_db.last_entered_lesson(student_username)
            client_obj.send(answer.encode())

        elif data[0] == Objects.Enum.ADD_FEEDBACK:
            student_username = data[1]
            lesson_number = data[2]
            verbal_feedback = data[3]
            quantitative_feedback = data[4]
            feedbacks_db.add_feedback(student_username, lesson_number, verbal_feedback, quantitative_feedback)

        elif data[0] == Objects.Enum.FEEDBACKS_PER_LESSON:
            student_username = data[1]
            lesson_number = data[2]
            answer = feedbacks_db.feedback_per_lesson(student_username, lesson_number)
            client_obj.send(answer.encode())

        elif data[0] == Objects.Enum.SHARE_FEEDBACK_WITH_FRIEND:
            lesson_number = data[1]
            student_username = data[2]
            friend_username = data[3]
            feedback_data = feedbacks_db.feedback_per_lesson(student_username, lesson_number)
            message = f"Feedback%{friend_username}%{student_username}%{feedback_data}".encode()  # Split with "%"
            connected_users[friend_username].send(message)
            # The thread activated on "friend_gets_feedback" func will get this message and show the friend the feedback

        elif data[0] == Objects.Enum.REMOVE_STUDENT:
            student_username = data[1]
            feedbacks_db.remove_student(student_username)  # Teacher decides to remove their student

            if student_username in connected_users.keys():  # If the student is connected, they are immediately removed
                connected_users[student_username].send("The Previous Frame".encode())

        elif data[0] == Objects.Enum.IF_REMOVED:
            student_username = data[1]
            answer = feedbacks_db.if_removed(student_username)
        # Checks if the student has been removed and, if so, returns their feedback data
            client_obj.send(pickle.dumps(answer))

        elif data[0] == Objects.Enum.STOP_THE_THREAD:
            client_obj.send("STOP THE THREAD".encode())

        elif data[0] == Objects.Enum.LOGOUT:
            username = data[1]
            if username in connected_users.keys():
                del connected_users[username]  # Removes the user from the dictionary


def accept_clients():
    """
    Accepts new clients connecting to the server and starts a thread to handle each client individually.

    This function continuously listens for incoming client connections. When a new client connects, it accepts
    the connection, retrieves the client object and the client's IP address, and then starts a new thread to handle
    that client. Each client is handled separately in its own thread, allowing the server to handle multiple clients
    concurrently.
    """
    while True:
        client_obj, ip = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_obj,)).start()


if __name__ == "__main__":
    threading.Thread(target=accept_clients).start()
