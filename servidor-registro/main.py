import socket

from server import Server 

def client_usecase(data):
    print(data)
    pass

def main():
    s = Server()
    s.run(client_usecase)
    pass

if __name__ == '__main__':
    main()