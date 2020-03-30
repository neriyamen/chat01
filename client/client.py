from connect import CONNECT
from chat import CHAT
from format import *
from _thread import *

HOST = '127.0.0.1'

class CLIENT:
    def __init__(self):
        self.connection = CONNECT(HOST, PORT)
        self.chat = CHAT()

    def start_connection(self):
        #open connection with the server
        message_type = ''
        self.connection.connect_to_server()
        while message_type != START_MESSAGE:
            self.chat.login()
            start_message = self.chat.create_start_message()
            self.connection.send_message(start_message)
            data = self.connection.get_message()
            message_type, message = self.chat.split_data(data)
            if message_type != START_MESSAGE:
                print('user name is already exist')
        self.chat.start_chat(self.create_room, self.join_room)

    def create_room(self):
        #create a new room, in the server side too
        self.connection.send_message(CREATE_SIGN)
        answer = self.connection.get_message()
        if answer == FAILED_MESSAGE:
            print('create room faild')
        else:
            self.chat.room_id = answer
            print('your room id is', answer)
            self.chat_mode()

    def join_room(self):
        #join to chat room, in the server side too
        answer = ''
        while answer != SUCCESS_MESSAGE:
            room_id = input('Enter room id: ')
            self.chat.room_id = room_id
            self.connection.send_message(JOIN_SIGN + SPLIT_CHAR + room_id)
            answer = self.connection.get_message()
            if answer == FAILED_MESSAGE:
                print('wrong room id')
        self.chat_mode()

    def chat_mode(self):
        # enter the user to chat mode, send message to the chat room and printing chat room messages.
        print('chat mode')
        new_message = ''
        start_new_thread(self.printing_chat_message, ())
        while new_message != EXIT_SIGN:
            new_message = input()
            self.connection.send_message(self.chat.create_chat_message(new_message))

    def printing_chat_message(self):
        # its thread in chat mode, printing all server message (chat room message).
        while True:
            message = self.connection.get_message()
            print(message)

def main():
    client = CLIENT()
    client.start_connection()

if __name__ == '__main__':
    main()
