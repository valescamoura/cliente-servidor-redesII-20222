import socket
from _thread import *
from core.server import Server
# import core.audio
import json

register_connect = socket.socket()
call_connect = socket.socket()
is_on_call = False
call_client = None # conectado a vc
call_user = None # vc está tentando conectar
print('Waiting for connection response')
def connect_to_register(register_server_host, register_server_port):
    try:
        register_connect.connect((register_server_host, register_server_port))
    except socket.error as e:
        print(str(e))

def connect_to_call(call_server_host, call_server_port, client_name):
    try:
        call_connect.connect((call_server_host, call_server_port))
        call_connect.send(json.dumps({ 'user': client_name }).encode('utf-8'))
        print('awaiting for response')
        data = call_connect.recv(2048).decode('utf-8')
        print('response received')
        return data
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

def onconnect_receiver(client, connection):
    global call_client
    global call_user
    call_client = json.loads(client)['user']
    print('receiving call from : ' + call_client)
    print('call_user: ' + str(call_user))
    print('\n')
    if call_user is not None and call_user['name'] == call_client:
        connection.send(json.dumps({ 'response': True }).encode('utf-8'))


def sender_use_case(data):
    #call_connect.send('connect request'.encode())
    call_connect.send('sample'.encode('utf-8'))
    while True:
        
        # ClientMultiSocket.send(core.audio.record())
    
        pass

def receiver_use_case(data):
    print(data)
    # core.audio.play(data)
    return 'aa'

connect_to_register('127.0.0.1', 53402)

nome = input('Insira seu nome de usuário: ')
s = Server(port=0)
start_new_thread(s.run, (receiver_use_case,onconnect_receiver)) # subindo servidor para receber áudio no cliente
register(nome, s.port) # cadastrando o usuário

op = input('(A) - Aceitar um ligação \n (R) - Rejeitar uma ligação \n (L) - Ligar para alguém')

print(call_client)
if op == 'A' and call_client is not None:
    is_on_call = True
    call_user = get_user(call_client)

    connect_to_call(call_user['ip'], call_user['port'], nome)
    start_new_thread(sender_use_case, (None,)) # rotina para enviar áudio pro cliente
    s.connection.send(json.dumps({ 'response': True }).encode('utf-8'))
elif op == 'R':
    is_on_call = False
    call_client = None
elif op == 'L':
    is_on_call = False
    nome_ligacao = input('Insira o nome de quem você quer ligar: ')

    call_user = get_user(nome_ligacao)
    answer = connect_to_call(call_user['ip'], call_user['port'], nome)
    accepted = json.loads(answer)
    if accepted['response']:
        start_new_thread(sender_use_case, (None,)) # rotina para enviar áudio pro cliente
    else:
        #lógica para quando usuário não aceitar a ligação
        pass
    print(accepted['response'])


op = input('Insira uma das opções: (D) Desligar chamada ou (R) Recomeçar programa')

#lógica para quando desligar a chamada ou recomeçar o programa
# if op == 'D' and call_client is not None:
#     is_on_call = False
#     start_new_thread(sender_use_case, (None,)) # rotina para enviar áudio pro cliente
# elif op == 'R':
#     is_on_call = False
#     call_client = None
# elif op == 'L':
#     is_on_call = False
#     nome_ligacao = input('Insira o nome de quem você quer ligar: ')


# ClientMultiSocket.close()