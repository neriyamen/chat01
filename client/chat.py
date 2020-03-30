from format import *

class CHAT:
    def __init__(self):
        user_name = ''

    def login(self):
        # take user name from the user
        self.user_name = input('user name: ')

    def create_start_message(self):
        # create the start message for sending to the server
        return 'start' + SPLIT_CHAR + self.user_name

    def split_data(self, data):
        # split the messages from the server
        if SPLIT_CHAR in data:
            return data.split(SPLIT_CHAR)
        return data, ''

    def start_chat(self, create_room, join_room):
        # start the program after created connection
        print('Welcome', self.user_name)
        self.menu(create_room, join_room)

    def menu(self, create_room, join_room):
        # manger the interface with the user
        its_leagal_selection = False
        while not its_leagal_selection:
            user_select = self.take_user_select()
            if user_select == '1':
                create_room()
                its_leagal_selection = True
            elif user_select == '2':
                join_room()
                its_leagal_selection = True
            else:
                print('Invalid selection')

    def take_user_select(self):
        # print menu and allowing choosing
        print('menu:')
        print('1. Create a chat room')
        print('2. Join a chat room')
        return input('Select an action(1/2): ')

    def create_chat_message(self, message):
        # create chat message according to the format
        return SEND_MESSAGE_SIGN + SPLIT_CHAR + message
