import socket
import threading
import Encryption
import DBhandle
import pickle
import Objects

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 4444))
server_socket.listen()

connected_clients = {}


def handle_client(client_obj):
    """
    :param client_obj: ID of the client
    :return: custom replay to each request specifically
    """
    while True:
        data = client_obj.recv(1024).decode().split('*')
        if not data:
            break

        if data[0] == Objects.Enum.REGISTRATION:
            username = data[1]
            password = data[2]
            user_type = data[3]
            answer = DBhandle.registration_process(username, Encryption.encrypted_password(password), user_type)
            if answer == user_type:
                connected_clients[username] = client_obj
            client_obj.send(answer.encode())
        elif data[0] == Objects.Enum.CONNECTING:
            username = data[1]
            password = data[2]
            answer = DBhandle.login_process(username, Encryption.encrypted_password(password))
            if answer in ["Student", "Teacher", "Friend"]:
                connected_clients[username] = client_obj
            client_obj.send(answer.encode())
        elif data[0] == Objects.Enum.YES:
            username = data[1]
            DBhandle.add_student("YES", username)
        elif data[0] == Objects.Enum.NO:
            username = data[1]
            DBhandle.add_student("NO", username)
        elif data[0] == Objects.Enum.STUDENT_LIST:
            list1 = DBhandle.list_of_students(1)
            list2 = DBhandle.list_of_students(2)
            list3 = DBhandle.list_of_students(3)
            check = [e for e in connected_clients.keys() if e in list1]
            result = check + list2
            result = [e for e in result if e not in list3 and e is not None]
            client_obj.send(pickle.dumps(result))
        elif data[0] == Objects.Enum.DISCONNECT:
            username = data[1]
            if username in connected_clients.keys():
                del connected_clients[username]
        elif data[0] == Objects.Enum.THE_NEXT_FRAME:
            student_username = data[1]
            teacher_username = data[2]
            if student_username in connected_clients.keys():
                connected_clients[student_username].send("The Next Frame".encode())
            DBhandle.add_users_to_feedbacks(student_username, teacher_username)
        elif data[0] == Objects.Enum.STUDENTS_FOR_TEACHER:
            teacher_username = data[1]
            client_obj.send(pickle.dumps(DBhandle.list_of_students_per_teacher(teacher_username)))
        elif data[0] == Objects.Enum.ADD_FEEDBACKS:
            student_username = data[1]
            lesson_number = data[2]
            verbal_feedback = data[3]
            quantitative_feedback = data[4]
            DBhandle.add_feedbacks(student_username, lesson_number, verbal_feedback, quantitative_feedback)
        elif data[0] == Objects.Enum.STEP2:
            teacher_username = data[1]
            client_obj.send(str(DBhandle.step2(teacher_username)).encode())
        elif data[0] == Objects.Enum.STEP1:
            teacher_username = data[1]
            client_obj.send(str(DBhandle.step1(teacher_username)).encode())
        elif data[0] == Objects.Enum.LAST_LESSON:
            student_username = data[1]
            client_obj.send(DBhandle.last_lesson(student_username).encode())
        elif data[0] == Objects.Enum.ADD_LESSON:
            student_username = data[1]
            teacher_username = data[2]
            DBhandle.add_lesson(student_username, teacher_username)
        elif data[0] == Objects.Enum.HOW_MUCH_LESSONS:
            student_username = data[1]
            client_obj.send((DBhandle.how_much_lessons(student_username)).encode())
        elif data[0] == Objects.Enum.FEEDBACKS_PER_LESSON:
            student_username = data[1]
            lesson_number = data[2]
            client_obj.send(DBhandle.feedback_per_lesson(student_username, lesson_number).encode())
        elif data[0] == Objects.Enum.FRIEND_LIST:
            check = DBhandle.friends_list()
            check = [e for e in connected_clients.keys() if e in check]
            client_obj.send(pickle.dumps(check))
        elif data[0] == Objects.Enum.SHARE_FEEDBACK_WITH_FRIEND:
            lesson_number = data[1]
            student_username = data[2]
            friend_username = data[3]
            connected_clients[friend_username].send(f"Feedback&{friend_username}&{student_username}"
                                                    f"&{DBhandle.feedback_per_lesson(student_username, lesson_number)}".encode())
        elif data[0] == Objects.Enum.REMOVE_STUDENT:
            student_username = data[1]
            DBhandle.remove_student(student_username)
            if student_username in connected_clients.keys():
                connected_clients[student_username].send("The Previous Frame".encode())
        elif data[0] == Objects.Enum.HEY:
            client_obj.send("HEY".encode())
        elif data[0] == Objects.Enum.IF_REMOVED:
            student_username = data[1]
            answer = DBhandle.if_removed(student_username)
            print(answer)
            client_obj.send(pickle.dumps(answer))



def accept_clients():
    """
    :return: accept new clients to the system and creates a thread
    """
    while True:
        client_obj, ip = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_obj,)).start()


if __name__ == "__main__":
    threading.Thread(target=accept_clients).start()