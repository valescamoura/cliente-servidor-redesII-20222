import socket
import os
from _thread import *

from core.constants import REGISTER_SERVER_IP

class Server:
    def __init__(self, port=5000, protocol='TCP'):
        self.protocol = protocol
        if self.protocol == 'TCP':
            self.server_side_socket = socket.socket()
        else:
            self.server_side_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        self.server_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.port = port
        self.threadCount = 0
        self.connection = self.server_side_socket
        self.init_server()

    def init_server(self):
        try:
            self.server_side_socket.bind((REGISTER_SERVER_IP, self.port)) # setando ip e porta 
        except socket.error as e:
            print(str(e))
        
        if self.protocol == 'TCP': 
            self.server_side_socket.listen(5) # iniciando escuta
        ip, port = self.server_side_socket.getsockname()
        self.ip = ip
        self.port = port
        print(f'Socket is listening on port {self.port} and ip {self.ip}')

    def run(self, client_usecase, onconnect=None, multithread=True): # multi-threaded client
        if multithread:
            while True:
                Client, address = self.server_side_socket.accept()
                if onconnect is not None:
                    data = Client.recv(4096)
                    onconnect(data.decode('utf-8'), Client)
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                start_new_thread(self.tcp_client_message_handler, (Client, client_usecase))
                self.threadCount += 1
                print('Thread Number: ' + str(self.threadCount))
        else:
            if onconnect is not None:
                data, address = self.server_side_socket.recvfrom(4096)
                onconnect(data.decode('utf-8'), self.server_side_socket)
                print('Connected to: '  + address[0] + ':' + str(address[1]))

            start_new_thread(self.udp_client_message_handler, (self.connection, client_usecase))
            self.threadCount += 1
            print('Thread Number: ' + str(self.threadCount))

    def udp_client_message_handler(self, connection, client_usecase):
        try:
            while True:
                data, address = connection.recvfrom(4096)
                response = client_usecase(data)
                # print("Received server data: " + str(data))
                if not data:
                    break
                # print('Sending data to client: ' + str(response))
        except ConnectionResetError:
            print(f'Connection ended for port: {self.port}')
            return None           

    def tcp_client_message_handler(self, connection, client_usecase):
        try:
            while True:
                data = connection.recv(4096)
                response = client_usecase(data)
                # print("Received server data: " + str(data))
                if not data:
                    break
                # print('Sending data to client: ' + str(response))
                if response is not None:
                    connection.sendall(str.encode(response))
                    
            connection.close()
        except ConnectionResetError:
            print(f'Connection ended for port: {self.port}')
            return None
