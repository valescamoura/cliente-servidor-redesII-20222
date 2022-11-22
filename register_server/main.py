import socket, pickle
from json import loads, dumps, JSONDecodeError
from register import Register
from core.server import Server 
from core.user import User
from core.request import Request
from register_server import register

register_clients = Register()

#
# data format
# data = { op: str, body: Union[str, User]}
#
def client_usecase(data: str):
    decoded_data = data.decode('utf-8')

    try:
        data = loads(decoded_data)
    except JSONDecodeError:
        return dumps('not valid message')


    print('Data receveid in client_usecase: ' + dumps(data))
    
    response = ''
    if data['op'] == 'register':
        user = data['body']
        response = register_clients.add_user(user)
        print(register_clients.table)
    elif data['op'] == 'unregister':
        user_name = data['body']
        response = register_clients.remove_user(user_name)
    elif data['op'] == 'get_user':
        user_name = data['body']
        response = register_clients.get_user(user_name)
    elif data['op'] == 'get_users':
        response = register.get_user()
    else:
        response = 'Opção não cadastrada'

    print(register_clients.table)
    return dumps(response)

def main():
    register_server = Server()
    register_server.run(client_usecase)

if __name__ == '__main__':
    main()
