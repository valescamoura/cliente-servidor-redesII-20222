import socket
import os
from _thread import *

class Server:
    def __init__(self, port=5000):
        self.server_side_socket = socket.socket()
        self.port = port
        self.threadCount = 0
        self.init_server()

    def init_server(self):
        try:
            self.server_side_socket.bind(('127.0.0.1', self.port))
        except socket.error as e:
            print(str(e))
        
        self.server_side_socket.listen(5)
        ip, port = self.server_side_socket.getsockname()
        self.ip = ip
        self.port = port
        print(f'Socket is listening on port {self.port} and ip {self.ip}')

    def run(self, client_usecase):
        while True:
            Client, address = self.server_side_socket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.client_message_handler, (Client, client_usecase))
            self.threadCount += 1
            print('Thread Number: ' + str(self.threadCount))

    def client_message_handler(self, connection, client_usecase):
        while True:
            data = connection.recv(2048)
            response = client_usecase(data)
            print("Received server data: " + str(data))
            if not data:
                break
            print('Sending data to client: ' + response)
            connection.sendall(str.encode(response))
        connection.close()

    def close(self):
        self.server_side_socket.close()
