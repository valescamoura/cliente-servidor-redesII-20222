import socket
from _thread import *
from core.server import Server
import core.audio
import json

register_connect = socket.socket()
call_connect = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
is_on_call = False
ip_address = None
call_client = None # conectado a vc
call_user = None # vc está tentando conectar
print('Waiting for connection response')

def get_ip():
    global ip_address
    dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns.connect(('8.8.8.8', 80))

    ip_address = dns.getsockname()[0]
    print(ip_address)
    dns.close

get_ip()

def connect_to_register(register_server_host, register_server_port):
    try:
        register_connect.connect((register_server_host, register_server_port))
    except socket.error as e:
        print(str(e))

def connect_to_call(call_server_host, call_server_port, client_name, need_answer = True):
    try:
        data = None
        call_connect.sendto(json.dumps({ 'user': client_name }).encode('utf-8'), (call_server_host, call_server_port))
        print('awaiting for response')
        if need_answer: 
            data = call_connect.recvfrom(1024).decode('utf-8')
        print('response received')
        return data
    except socket.error as e:
        print(str(e))

def register(client_name, port):
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
        connection.sendto(json.dumps({ 'response': True }).encode('utf-8'), (call_user['ip'], call_user['port']))


def sender_use_case(_):
    #call_connect.send('connect request'.encode())
    i = 0
    while True:  
        if i% 20 == 0:
            call_connect.sendto(core.audio.record(), (call_user['ip'], call_user['port']))
        i+=1

def receiver_use_case(data):
    if data:
        audio.play(data)
    return 'a'

connect_to_register('192.168.0.40', 57391)

nome = input('Insira seu nome de usuário: ')
s = Server(port=0, protocol='UDP')
start_new_thread(s.run, (receiver_use_case,onconnect_receiver, False)) # subindo servidor para receber áudio no cliente
register(nome, s.port) # cadastrando o usuário

while True:
    op = input('(A) - Aceitar um ligação \n (R) - Rejeitar uma ligação \n (L) - Ligar para alguém')

    print(call_client)
    if op == 'A' and call_client is not None:
        is_on_call = True
        call_user = get_user(call_client)

        #connect_to_call(call_user['ip'], call_user['port'], nome, False)
        start_new_thread(sender_use_case, (None,)) # rotina para enviar áudio pro cliente
        s.connection.sendto(json.dumps({ 'response': True }).encode('utf-8'), (call_user['ip'], call_user['port']))

        op = input('Pressione qualquer tecla para finalizar a chamada:')
    elif op == 'R':
        is_on_call = False
        call_client = None
        s.connection.sendto(json.dumps({ 'response': False }).encode('utf-8'), (call_user['ip'], call_user['port']))
    elif op == 'L':
        is_on_call = False
        nome_ligacao = input('Insira o nome de quem você quer ligar: ')

        call_user = get_user(nome_ligacao)
        answer = connect_to_call(call_user['ip'], call_user['port'], nome)
        accepted = json.loads(answer)
        if accepted['response']:
            start_new_thread(sender_use_case, (None,)) # rotina para enviar áudio pro cliente

            op = input('Pressione qualquer tecla para finalizar a chamada:')
        else:
            call_user = None
            call_client = None
            #lógica para quando usuário não aceitar a ligação



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