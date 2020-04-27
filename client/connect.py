import socket

BUFFER_SIZE = 1024

class CONNECT:
    def __init__(self, host, port):
        """
        take care to the connection with the server.
        :param host: string type, ip of the server
        :param port: int type, the port where server listening
        :return: none
        """
        self.host = host
        self.port = port
        self.socket = None

    def connect_to_server(self):
        """
        create socket and make tha first connection with the server.
        :return: none
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except ConnectionError as e:
            print (e)
            exit()

    def get_message(self):
        """
        receiver new message from the server.
        :return: string type, new server message
        """
        try:
            message = self.socket.recv(BUFFER_SIZE).decode("utf-8")
            return message
        except ConnectionError as e:
            print (e)
            exit()

    def send_message(self, data):
        """
        send a message to the server
        :param data: string type, message to server
        :return: none
        """
        try:
            self.socket.sendall(data.encode())
        except ConnectionError as e:
            print (e)
            exit()
