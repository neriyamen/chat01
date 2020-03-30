class USER:
    def __init__(self, client_socket):
        # create a new user
        self.room_id = 0
        self.user_name = ''
        self.user_socket = client_socket
        self.connected = True

    def send_message(self, data):
        # send message to the user
        self.user_socket.send(data.encode())

    def get_message(self):
        # get message from the user
        try:
            return self.user_socket.recv(1024).decode("utf-8")
        except:
            print(self.user_socket.getpeername(), 'is unconnected')
            self.connected = False
            self.user_socket.close()
