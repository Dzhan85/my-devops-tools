import socket
import sys
import os


host = sys.argv[1]
port = int(sys.argv[2])


RECV_SIZE = 256
DATA_TO_SEND = "test".encode()

try:

    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.connect((host, port))

    mysock.send(DATA_TO_SEND)
    data = mysock.recv(RECV_SIZE)

except ConnectionRefusedError as e:
    exit(1)

if len(data) >= 0:
    exit(0)
else:
    exit(1)
