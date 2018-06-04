import socket
import time
import re
import random
import subprocess
import sys

HOST, PORT = "10.112.108.77", int(1111)

DEBUG = True
GAP = 0.4


def send(sock, s):
    sock.send(str.encode(s + '\n'))
    if DEBUG:
        print(s)
    time.sleep(GAP)


def recv(sock):
    receive = bytes.decode(sock.recv(40960))
    if DEBUG:
        print(receive)
    return receive


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

time.sleep(GAP)

receive = recv(sock)
send(sock, "yes")

receive = recv(sock)
receive = receive[(re.search(r"#", receive).span()[0]):-21]




p = subprocess.Popen('./zelda', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
p.stdin.write(receive.encode())
sock.send(p.communicate()[0])
time.sleep(0.5)

receive = recv(sock)

ans = input()
send(sock, ans)
recv(sock)

sock.close()
