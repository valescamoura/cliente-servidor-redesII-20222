import socket

from server import Server 

clients = []

def client_usecase(data):
    print('robson : ' + str(data))
    
    return 'ablabluble'

def main():
    s = Server()
    s.run(client_usecase)
    pass

if __name__ == '__main__':
    main()