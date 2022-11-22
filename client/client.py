import socket
import sys
from _thread import *
from core.server import Server
import core.audio
import json
import base64

register_connect = socket.socket()
call_connect = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
is_on_call = False
ip_address = None
call_client = None # conectado a vc
call_user = None # vc está tentando conectar
print('Waiting for connection response')

register_server_ip = str(sys.argv[1])

def get_ip():
    global ip_address
    dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns.connect(('8.8.8.8', 80))

    ip_address = dns.getsockname()[0]
    print(f'My ip address: {ip_address}')
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
        call_connect.sendto(json.dumps({ 'op': 'control', 'user': client_name }).encode('utf-8'), (call_server_host, call_server_port))
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
    print(client)
    global call_client
    global call_user
    info = json.loads(client)
    print(client)
    call_client = info['op'] == 'control' and info['user']

    if call_user is not None and call_user['name'] == call_client and info['op'] == 'control':
        print('receiving call from : ' + call_client)
        print('call_user: ' + str(call_user))
        print('\n')
    if call_user is not None and call_user['name'] == call_client:
        connection.sendto(json.dumps({ 'op': 'control', 'response': True, 'user': nome }).encode('utf-8'), (call_user['ip'], call_user['port']))

def sender_use_case(_):
    #call_connect.send('connect request'.encode())
    
    while is_on_call:  
        call_connect.sendto(json.dumps({'op': 'audio', 'audio': base64.b64encode(core.audio.record()).decode('utf-8')}).encode('utf-8'), (call_user['ip'], call_user['port']))


def receiver_use_case(data):
    global is_on_call
    r = json.loads(data.decode('utf-8'))
    if is_on_call:
    if r['op'] == 'disable':
        is_on_call = False
        print('chamada encerrada')
    if is_on_call:
        if r['op'] == 'audio':
            core.audio.play(base64.b64decode(r['audio'].encode('utf-8')))

connect_to_register(register_server_ip, 5005)

nome = input('Insira seu nome de usuário: ')
s = Server(port=6000, protocol='UDP')
start_new_thread(s.run, (receiver_use_case,onconnect_receiver, False)) # subindo servidor para receber áudio no cliente
register(nome, s.port) # cadastrando o usuário

while True:
    op = input('(A) - Aceitar um ligação \n (R) - Rejeitar uma ligação \n (L) - Ligar para alguém')

    print(call_client)
    if op == 'A' and call_client is not None:
        is_on_call = True
        call_user = get_user(call_client)

        #connect_to_call(call_user['ip'], call_user['port'], nome, False)
        s.connection.sendto(json.dumps({ 'op': 'control', 'response': True, 'user': nome }).encode('utf-8'), (call_user['ip'], call_user['port']))
        call_connect.sendto(json.dumps({ 'op': 'control', 'response': True, 'user': nome }).encode('utf-8'), (call_user['ip'], call_user['port']))
        start_new_thread(sender_use_case, (None,)) # rotina para enviar áudio pro cliente

        op = input('Pressione qualquer tecla para finalizar a chamada:')
    elif op == 'R':
        is_on_call = False
        if call_client is None:
            continue

        call_user = get_user(call_client)
        s.connection.sendto(json.dumps({ 'op': 'control', 'response': False, 'user': nome }).encode('utf-8'), (call_user['ip'], call_user['port']))
    elif op == 'L':
        is_on_call = False
        nome_ligacao = input('Insira o nome de quem você quer ligar: ')

        call_user = get_user(nome_ligacao)
        answer = connect_to_call(call_user['ip'], call_user['port'], nome)  
        print('awaiting for response')
        a, data = s.connection.recvfrom(1024)
        if data[0] == call_user['ip']:
            response = json.loads(a.decode('utf-8'))
        print(response)
        if data[0] == call_user['ip'] and response['response']:
            print('accepted')
            is_on_call = True
            thread_id = start_new_thread(sender_use_case, (None,)) # rotina para enviar áudio pro cliente

            op = input('Pressione qualquer tecla para finalizar a chamada:')
            if is_on_call:
                print("sending close")
                call_connect.sendto(json.dumps({'op': 'disable'}).encode('utf-8'), (call_user['ip'], call_user['port']))
                is_on_call = False
            call_client = None
            call_user = None
        else:
            call_user = None
            call_client = None
            print('not accepted')
            #lógica para quando usuário não aceitar a ligação


#lógica para quando desligar a chamada ou recomeçar o programa


# ClientMultiSocket.close()