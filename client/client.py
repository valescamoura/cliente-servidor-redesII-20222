import socket
from _thread import *
from core.server import Server
# import core.audio
import json

register_connect = socket.socket()
call_connect = socket.socket()
print('Waiting for connection response')
def connect_to_register(register_server_host, register_server_port):
    try:
        register_connect.connect((register_server_host, register_server_port))
    except socket.error as e:
        print(str(e))

def connect_to_call(call_server_host, call_server_port):
    try:
        call_connect.connect((call_server_host, call_server_port))
    except socket.error as e:
        print(str(e))

def register(client_name, port):

    ip_address=socket.gethostbyname(socket.gethostname())
    register_connect.send(json.dumps({ 'op': 'register', 'body' : { 'name': client_name, 'ip': ip_address, 'port': port}}).encode('utf-8'))
    res = register_connect.recv(1024)
    print('server response: ' + res.decode('utf-8'))
    return res

def unregister(client_name):
    register_connect.send(json.dumps({ 'op': 'unregister', 'body' : client_name}).encode('utf-8'))
    res = register_connect.recv(1024)
    print('server response: ' + res.decode('utf-8'))
    return res

def get_user(client_name):
    register_connect.send(json.dumps({ 'op': 'get_user', 'body' : client_name}).encode('utf-8'))
    res = register_connect.recv(1024)
    print('server response: ' + res.decode('utf-8'))
    return json.loads(res.decode('utf-8'))

def receiver_use_case(data):
    print(data)
    # core.audio.play(data)
    return 'aa'

def sender_use_case(data):
    call_connect.send('connect request'.encode())
    # while True:
    #     # ClientMultiSocket.send(core.audio.record())
    #     pass


connect_to_register('127.0.0.1', 52545)

nome = input('Insira seu nome de usuário: ')
s = Server(port=0)
start_new_thread(s.run, (receiver_use_case,)) # subindo servidor para receber áudio no cliente
register(nome, s.port) # cadastrando o usuário

nome_ligacao = input('Deseja ligar para alguém? Insira o nome do usuário que deseja ligar: ')
call_user = get_user(nome_ligacao)

connect_to_call(call_user['ip'], call_user['port'])

start_new_thread(sender_use_case, (None,)) 

op = input('Insira uma das opções: (D) Desligar chamada ou (R) Recomeçar programa')



# ClientMultiSocket.close()