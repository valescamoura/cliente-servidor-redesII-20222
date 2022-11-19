import socket
from json import loads as json_loads
from json import dump as json_dump

from register_server.register import Register
from core.server import Server 
from core.user import User
from core.request import Request

register_clients = Register()

#
# data format
# data = { op: str, body: Union[str, User]}
#
def client_usecase(data: str):
    
    print('Data receveid in client_usecase: ' + data)
    data = json_loads(data)
    
    response = ''
    if data['op'] == 'register':
        user = data['body']
        response = register_clients.add_user(user)
        # print(register_clients.table)
    elif data['op'] == 'disconnect':
        user_name = data['body']
        response = register_clients.remove_user(user_name)
    elif data['op'] == 'connect_users':
        user_name = data['body']
        response = register_clients.get_user(user_name)
    else:
        response = 'Opção não cadastrada'

    return json_dump(response)

def main():
    register_server = Server()
    register_server.run(client_usecase)

if __name__ == '__main__':
    main()
