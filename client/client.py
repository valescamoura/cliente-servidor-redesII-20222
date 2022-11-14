import socket
import core.audio

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(1024)
while True:
    Input = input('Hey there: ')
    ClientMultiSocket.send(core.audio.record())
    res = ClientMultiSocket.recv(1024)
    core.audio.play(res)
    #print(res.decode('utf-8'))

ClientMultiSocket.close()