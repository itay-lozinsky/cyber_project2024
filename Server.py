import socket
import threading
import HashMD5
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
            answer = DBhandle.create_user(username, HashMD5.hash(password), user_type)
            if answer == user_type:
                connected_clients[username] = client_obj
            client_obj.send(answer.encode())
        elif data[0] == Objects.Enum.CONNECTING:
            username = data[1]
            password = data[2]
            answer = DBhandle.check_password(username, HashMD5.hash(password))
            if answer in ["Student", "Teacher", "Friend"]:
                connected_clients[username] = client_obj
            client_obj.send(answer.encode())
        elif data[0] == Objects.Enum.IS_JOINED:
            student_username = data[1]
            client_obj.send(str(DBhandle.is_joined(student_username)).encode())
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
            list1 = [item for t in list1 for item in t]
            list3 = [item for t in list3 for item in t]
            check = [e for e in connected_clients.keys() if e in list1]
            print(list3)
            if check:
                result = check + list2
                result = [e for e in list3 if e not in result]
                client_obj.send(pickle.dumps(result))
            else:
                result = list2
                result = [e for e in list3 if e not in result]
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
            client_obj.send(pickle.dumps(DBhandle.list_of_students_for_teacher(teacher_username)))
        elif data[0] == Objects.Enum.ADD_FEEDBACKS:
            student_username = data[1]
            lesson_number = data[2]
            verbal_feedback = data[3]
            quantitative_feedback = data[4]
            DBhandle.add_feedbacks(student_username, lesson_number, verbal_feedback, quantitative_feedback)
        elif data[0] == Objects.Enum.CHECK_IF_FIRST_TIME_CONNECTED:
            teacher_username = data[1]
            client_obj.send(str(DBhandle.check_if_first_time_connected(teacher_username)).encode())
        elif data[0] == Objects.Enum.LAST_LESSON:
            student_username = data[1]
            client_obj.send(DBhandle.last_lesson(student_username).encode())
        elif data[0] == Objects.Enum.ADD_LESSON:
            student_username = data[1]
            teacher_username = data[2]
            DBhandle.add_lesson(student_username, teacher_username)
        elif data[0] == Objects.Enum.HOW_MUCH_LESSONS:
            student_username = data[1]
            DBhandle.how_much_lessons(student_username)



def accept_clients():
    """
    :return: accept new clients to the system and creates a thread
    """
    while True:
        client_obj, ip = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_obj,)).start()


if __name__ == "__main__":
    threading.Thread(target=accept_clients).start()