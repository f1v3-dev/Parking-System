import socket

HOST = '172.30.1.32'
PORT = 3001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))


while True:
    message = b'fucking pi'
    s.sendall(message)
