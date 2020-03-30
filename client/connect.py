import socket

BUFFER_SIZE = 1024

class CONNECT:
    # take care to the connection with the server.
    def __init__(self, host, port):
        #this is the constructor that takes in host and port.
        self.host = host
        self.port = port
        self.socket = None

    def connect_to_server(self):
        # create socket and make tha first connection with the server.
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except:
            print('connection error')
            exit()


    def get_message(self):
        # receiver new message from the server.
        try:
            return self.socket.recv(BUFFER_SIZE).decode("utf-8")
        except:
            print('connection error')
            exit()

    def send_message(self, data):
        # send a message to the server
        try:
            self.socket.sendall(data.encode())
        except:
            print('connection error')
            exit()
