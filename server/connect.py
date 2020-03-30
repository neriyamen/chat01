import socket

BUFFER_SIZE = 1024
MAX_USER_CAPACITY = 10

class CONNECT:
    def __init__(self, port):
        # create socket for the server
        self.host = ''
        self.port = port
        self.socket = None

    def start_socket_listening(self):
        # start listening mode
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        print("socket binded to port", self.port)
        self.socket.listen(MAX_USER_CAPACITY)
        print("socket is listening...")

