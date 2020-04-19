import format

class CHAT:
    def __init__(self):
        user_name = ''

    def login(self):
        # take user name from the user
        self.user_name = input('user name: ')

    def create_START_CONNECTION_MESSAGE(self):
        # create the start message for sending to the server
        return 'start' + format.SPLIT_TYPE_AND_DATA_CHAR + self.user_name

    @staticmethod
    def split_data(data):
        # split the messages from the server
        if format.SPLIT_TYPE_AND_DATA_CHAR in data:
            return data.split(format.SPLIT_TYPE_AND_DATA_CHAR)
        return data, ''

    def start_chat(self, create_room, join_room):
        # start the program after created connection
        print('Welcome', self.user_name)
        self.menu(create_room, join_room)

    @classmethod
    def menu(cls, create_room, join_room):
        # manger the interface with the user
        its_leagal_selection = False
        while not its_leagal_selection:
            user_select = cls.take_user_select()
            if user_select == '1':
                create_room()
                its_leagal_selection = True
            elif user_select == '2':
                join_room()
                its_leagal_selection = True
            else:
                print('Invalid selection')

    @staticmethod
    def take_user_select():
        # print menu and allowing choosing
        print('menu:')
        print('1. Create a chat room')
        print('2. Join a chat room')
        return input('Select an action(1/2): ')

    @staticmethod
    def create_chat_message(message):
        # create chat message according to the format
        return format.SEND_MESSAGE_TO_REST_USERS_IN_ROOM_SIGN + format.SPLIT_TYPE_AND_DATA_CHAR + message
