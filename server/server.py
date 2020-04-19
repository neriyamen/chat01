from user import USER
from connect import CONNECT
from room import ROOM
import format
from _thread import *

class SERVER:
    def __init__(self, port):
        self.connection = CONNECT(port)
        self.rooms = {}
        self.users = {}

    def single_user(self, user):
        # thread function for any user
        while user.connected:
            data = user.get_message()
            if not user.connected:
                break
            self.treatment_of_message(user, data)
        self.exit_user(user)

    def treatment_of_message(self, user, message):
        # choose what to do with any message
        try:
            if format.SPLIT_TYPE_AND_DATA_CHAR in message:
                message_type, data = message.split(format.SPLIT_TYPE_AND_DATA_CHAR)
            else:
                message_type = message
            if message_type == format.START_CONNECTION_MESSAGE:
                self.start_user(user, data)
            elif message_type == format.CREATE_NEW_ROOM_SIGN:
                self.create_room(user)
            elif message_type == format.SEND_MESSAGE_TO_REST_USERS_IN_ROOM_SIGN:
                self.pass_message(user, data)
            elif message_type == format.JOIN_TO_ROOM_REQUEST_SIGN:
                self.join_room(user, data)
            elif message_type == format.EXIT_SIGN:
                self.exit_user(user)
        except:
            print('message is unrecogniz')
            user.send_message(format.FAILED_MESSAGE)

    def join_room(self, user, message):
        # joining user to chat room
        if int(message) in self.rooms:
            user.room_id = int(message)
            self.rooms[int(message)].join_room(user)
            user.send_message(format.SUCCESS_MESSAGE)
        else:
            user.send_message(format.FAILED_MESSAGE)

    def pass_message(self, user, message):
        # use in user's room pass_message method to pass message to rest of users.
        room_id = user.room_id
        room = self.rooms[room_id]
        room.pass_message(user, message)

    def start_user(self, user, user_name):
        # configure user in first connection.
        if user_name in self.users:
            user.send_message(format.USERNAME_IS_ALREADY_EXISTS_MESSAGE)
        else:
            user.user_name = user_name
            self.users[user_name] = user
            user.send_message(format.START_CONNECTION_MESSAGE)

    def create_room(self, user):
        # create a new room according to user request
        new_room = ROOM(user, self.rooms)
        self.rooms[new_room.room_id] = new_room
        user.room_id = new_room.room_id
        user.send_message(str(new_room.room_id))

    def exit_user(self, user):
        # care to user who leaving
        user.user_socket.close()
        del self.users[user.user_name]
        user_room = self.rooms[user.room_id]
        user_room.users.remove(user)
        if len(user_room.users) == 0:
            del self.rooms[user.room_id]

def main():
    server = SERVER(format.PORT)
    server.connection.start_socket_listening()
    while True:
        # establish connection with client
        client_socket, addr = server.connection.socket.accept()
        user = USER(client_socket)
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread for one user
        start_new_thread(server.single_user, (user,))
    server.connection.socket.close()

if __name__ == '__main__':
    main()
