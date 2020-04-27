import messages_format

class CHAT:
    def __init__(self):
        """
        chat tools for user
        """
        self.user_name = ''
        self.room_name = ''
        self.printing_chat_mode = False

    def login(self):
        """
        take user name from the user
        :return: none
        """
        self.user_name = input('user name: ')

    def create_start_message(self):
        """
        create the start message for sending to the server
        :return: string type, the start connection message
        """
        return 'start' + messages_format.SPLIT_TYPE_AND_DATA_CHAR + self.user_name

    @staticmethod
    def split_data(data):
        """
        split the messages from the server to message type and data
        :param data: string type, string to split
        :return: tuple type (string, string), message type and data
        """
        if messages_format.SPLIT_TYPE_AND_DATA_CHAR in data:
            return data.split(messages_format.SPLIT_TYPE_AND_DATA_CHAR)
        return data, ''

    def start_chat(self, asks_to_create_room, asks_to_join_room, close_connection):
        """
        start the program after created connection
        :param asks_to_create_room: function type, use to create room
        :param asks_to_join_room: function type, use to join to room
        :param close_connection: function type, use to close the connection with the server when user exit
        :return: none
        """
        print('Welcome', self.user_name)
        self.menu(asks_to_create_room, asks_to_join_room, close_connection)

    @classmethod
    def menu(cls, asks_to_create_room, asks_to_join_room, close_connection):
        """
        manger the interface with the user
        :param asks_to_create_room: function type, use to create room
        :param asks_to_join_room: function type, use to join to room
        :param close_connection: function type, use to close the connection with the server when user exit
        :return: none
        """
        user_select = ''
        while user_select != '3':
            user_select = cls.take_user_select()
            if user_select == '0':
                cls.print_manuel()
            elif user_select == '1':
                asks_to_create_room()
                its_leagal_selection = True
            elif user_select == '2':
                asks_to_join_room()
                its_leagal_selection = True
            elif user_select == '3':
                close_connection()
                print('bye')
            else:
                print('Invalid selection')

    @staticmethod
    def take_user_select():
        """
        print menu and allowing choosing
        :return: string type, the user's choice
        """
        print('menu:')
        print('0. manuel')
        print('1. Create a chat room')
        print('2. Join a chat room')
        print('3. exit')
        return input('Select an action(0/1/2/3): ')

    @staticmethod
    def print_manuel():
        """
        print the menual for the user
        :return:
        """
        print('Welcome to Chat!')
        print('in this program you can create room chat and enter to exists rooms')
        print('to joining to room press 2 and chose one of the room the program show you')
        print('to create a new room press 3 and enter name for the room')

    @staticmethod
    def create_chat_message(message):
        """
        create chat message according to the messages_format
        :param message: string type, the data from user
        :return: string type, the message to send to the server
        """
        return messages_format.SEND_MESSAGE_TO_REST_USERS_IN_ROOM_SIGN + messages_format.SPLIT_TYPE_AND_DATA_CHAR + message
