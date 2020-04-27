from user import USER
from connect import CONNECT
from room import ROOM
import messages_format
from _thread import *

class SERVER:
    def __init__(self, port):
        """
        multy-users server for chat project
        :param port: int type, the port to server listening
        :return: none
        """
        self.connection = CONNECT(port)
        self.rooms = {}
        self.users = {}

    def single_user(self, user):
        """
        thread function for any user
        :param user: USER type, the new user
        :return: none
        """
        while user.connected:
            data = user.get_message()
            if not user.connected:
                break
            self.treatment_of_message(user, data)

    def treatment_of_message(self, user, message):
        """
        choose what to do with any message
        :param user: USER type, user who send the message
        :param message: string type, the message from the user
        :return: none
        """
        if messages_format.SPLIT_TYPE_AND_DATA_CHAR in message:
            message_type, data = message.split(messages_format.SPLIT_TYPE_AND_DATA_CHAR)
        else:
            message_type = message
        if message_type == messages_format.START_CONNECTION_MESSAGE:
            self.start_user(user, data)
        elif message_type == messages_format.CREATE_NEW_ROOM_SIGN:
            self.create_room(user, data)
        elif message_type == messages_format.SEND_MESSAGE_TO_REST_USERS_IN_ROOM_SIGN:
            self.pass_message(user, data)
            if data == 'exit':
                self.leave_room(user)
        elif message_type == messages_format.JOIN_TO_ROOM_REQUEST_SIGN:
            self.join_room(user, data)
        elif message_type == messages_format.ROOMS_NAMES_REQUEST:
            self.send_rooms_names(user)
        elif message_type == messages_format.EXIT_SIGN:
            self.exit_user(user)

    def join_room(self, user, room_name):
        """
        joining user to chat room and send to user if success
        :param user: USER type, the new user at the room
        :param room_name: string type, the name of the room
        :return: none
        """
        if room_name in self.rooms:
            user.room_name = room_name
            self.rooms[room_name].join_room(user)
            self.pass_message(user, 'connected')
            user.send_message(messages_format.SUCCESS_MESSAGE)
        else:
            user.send_message(messages_format.FAILED_MESSAGE)

    def send_rooms_names(self, user):
        """
        send the names of all exists rooms to user
        :param user: USER type, the user to send the rooms names
        :return: none
        """
        rooms_names = ''
        if len(self.rooms) == 0:
            user.send_message(messages_format.NO_ROOMS_EXISTS)
        else:
            for room_name in self.rooms:
                rooms_names += room_name + '    '
            user.send_message(rooms_names)

    def pass_message(self, user, message):
        """
        use in user's room pass_message method to pass message to rest of users.
        :param user: USER TYPE, the owner of the message
        :param message: string type, the message to pass
        :return: none
        """
        room_name = user.room_name
        room = self.rooms[room_name]
        room.pass_message(user, message)

    def start_user(self, user, user_name):
        """
        configure user in first connection.
        :param user: USER type, the new user to config
        :param user_name: string type, name of the new user.
        :return:
        """
        if user_name in self.users:
            user.send_message(messages_format.USERNAME_IS_ALREADY_EXISTS_MESSAGE)
        else:
            user.user_name = user_name
            self.users[user_name] = user
            user.send_message(messages_format.START_CONNECTION_MESSAGE)

    def create_room(self, user, room_name):
        """
        create a new room according to user request
        :param user: USER type, the user who asks for create room
        :param room_name: string type, the name the user asks for is room
        :return: none
        """
        new_room = ROOM(room_name, user, self.rooms)
        if new_room.room_name == '':
            user.send_message(messages_format.ROOM_NAME_IS_ALREADY_EXISTS_MESSAGE)
        else:
            self.rooms[new_room.room_name] = new_room
            user.room_name = new_room.room_name
            user.send_message(messages_format.SUCCESS_MESSAGE)

    def exit_user(self, user):
        """
        care to user who leaving
        :param user: USER type, the user who leave his room
        :return: none
        """
        print(user.user_socket.getpeername(), 'is unconnected')
        user.connected = False
        user.user_socket.close()
        self.leave_room(user)
        if user.user_name != '':
            del self.users[user.user_name]

    def leave_room(self, user):
        """
        remove user from room and clear user's room field
        :param user: USER type, user who leaved room
        :return: none
        """
        if user.room_name != '':
            user_room = self.rooms[user.room_name]
            user_room.users.remove(user)
            if len(user_room.users) == 0:
                del self.rooms[user.room_name]
            user.room_name = ''
        if user.connected:
            user.send_message('you leaved room')

def main():
    server = SERVER(messages_format.PORT)
    server.connection.start_socket_listening()
    while True:
        # establish connection with client
        client_socket, addr = server.connection.socket.accept()
        user = USER(client_socket, server.exit_user)
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread for one user
        start_new_thread(server.single_user, (user,))
    server.connection.socket.close()

if __name__ == '__main__':
    main()
