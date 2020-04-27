from connect import CONNECT
from chat import CHAT
import messages_format
import _thread

HOST = '127.0.0.1'

class CLIENT:
    def __init__(self):
        """
        the client side in chat project
        :return: none
        """
        self.connection = CONNECT(HOST, messages_format.PORT)
        self.chat = CHAT()

    def start_connection(self):
        """
        open connection with the server
        :return: none
        """
        message_type = ''
        self.connection.connect_to_server()
        while message_type != messages_format.START_CONNECTION_MESSAGE:
            self.chat.login()
            start_connection_message = self.chat.create_start_message()
            self.connection.send_message(start_connection_message)
            data = self.connection.get_message()
            message_type, message = self.chat.split_data(data)
            if message_type != messages_format.START_CONNECTION_MESSAGE:
                print('user name is already exist')
        self.chat.start_chat(self.asks_to_create_room, self.asks_to_join_room, self.close_connection)

    def asks_to_create_room(self):
        """
        create a new room, in the server side too
        :return: none
        """
        room_name = input('enter room name: ')
        self.connection.send_message(messages_format.CREATE_NEW_ROOM_SIGN + messages_format.SPLIT_TYPE_AND_DATA_CHAR + room_name)
        answer = self.connection.get_message()
        if answer == messages_format.ROOM_NAME_IS_ALREADY_EXISTS_MESSAGE:
            print('error: room in is name is already exists')
        else:
            self.chat.room_name = room_name
            print('your room name is', room_name)
            self.chat_mode()

    def asks_to_join_room(self):
        """
        join to chat room, in the server side too
        :return: none
        """
        any_room_exists = self.show_rooms_names()
        if any_room_exists == True:
            answer = ''
            while answer != messages_format.SUCCESS_MESSAGE:
                room_name = input('Enter room name: ')
                self.connection.send_message(messages_format.JOIN_TO_ROOM_REQUEST_SIGN + messages_format.SPLIT_TYPE_AND_DATA_CHAR + room_name)
                answer = self.connection.get_message()
                if answer == messages_format.FAILED_MESSAGE:
                    print('wrong room name')
            self.chat.room_name = room_name
            self.chat_mode()

    def close_connection(self):
        """
        close connection with the server
        :return: none
        """
        self.connection.send_message(messages_format.EXIT_SIGN)
        self.connection.socket.close()

    def show_rooms_names(self):
        """
        asks from the server all names of rooms, and printing the list
        :return: bool type, true if rooms exists and false if any room is not exists
        """
        self.connection.send_message(messages_format.ROOMS_NAMES_REQUEST)
        rooms_names = self.connection.get_message()
        if rooms_names == messages_format.NO_ROOMS_EXISTS:
            print('no rooms exists')
            return False
        print('rooms: ')
        print('       ', rooms_names)
        return True

    def chat_mode(self):
        """
        enter the user to chat mode, send message to the chat room and printing chat room messages.
        :return: none
        """
        print('chat mode')
        new_message = ''
        _thread.start_new_thread(self.printing_chat_message, ())
        while new_message != 'exit':
            new_message = input()
            if new_message != '':
                self.connection.send_message(self.chat.create_chat_message(new_message))
        self.chat.room_name = ''
        while self.chat.printing_chat_mode:
            pass

    def printing_chat_message(self):
        """
        its thread in chat mode, printing all server message (chat room message).
        :return: none
        """
        self.chat.printing_chat_mode = True
        while self.chat.room_name != '':
            message = self.connection.get_message()
            print(message)
        self.chat.printing_chat_mode = False


def main():
    client = CLIENT()
    client.start_connection()


if __name__ == '__main__':
    main()
