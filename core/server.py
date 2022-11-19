import socket
import os
from _thread import *

class Server:
    def __init__(self, host='127.0.0.1', port=2004):
        self.server_side_socket = socket.socket()
        self.host = host
        self.port = port
        self.threadCount = 0
        self.init_server()

    def init_server(self):
        try:
            self.server_side_socket.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))

        print('Socket is listening..')
        self.server_side_socket.listen(5)

    def run(self, client_usecase):
        while True:
            Client, address = self.server_side_socket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.client_message_handler, (Client, client_usecase))
            self.threadCount += 1
            print('Thread Number: ' + str(self.threadCount))

    def client_message_handler(self, connection, client_usecase):
        connection.send(str.encode('Server is working:'))
        while True:
            data = connection.recv(2048)
            response = client_usecase(data.decode('utf-8'))
            print("Received server data: " + data.decode('utf-8'))
            if not data:
                break
            connection.sendall(str.encode(response))
        connection.close()

    def close(self):
        self.server_side_socket.close()
