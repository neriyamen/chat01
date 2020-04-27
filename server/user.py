class USER:
    def __init__(self, client_socket, exit_user):
        """
        single user
        :param client_socket: socket type, the socket between the server to the new client
        :param exit_user: function type, function for manger in case the client is cut off
        :return: none
        """
        self.room_name = ''
        self.user_name = ''
        self.user_socket = client_socket
        self.connected = True
        self.exit_user = exit_user

    def send_message(self, data):
        """
        send message to the user
        :param data: string type, data to send to the client
        :return: none
        """
        self.user_socket.send(data.encode())

    def get_message(self):
        """
        get message from the user
        :return: string type, new message from the client
        """
        try:
            return self.user_socket.recv(1024).decode("utf-8")
        except:
            self.exit_user(self)
