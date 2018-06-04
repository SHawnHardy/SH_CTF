import socket
import time
import re
import random
import subprocess
import sys

HOST, PORT = "10.112.108.77", int(1114)

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
receive = receive[(re.search(r"\d", receive).span()[0]):]
# print(receive)
test_num = int(receive[:re.search(r"\s", receive).span()[0]])
test_data = receive[(re.search(r"\s", receive).span()[0]):]

for i in range(test_num):
    if i > 0:
        receive = recv(sock)
        test_data = receive[(re.search(r"\d", receive).span()[0]):]


    p = subprocess.Popen('./party_of_god_ze', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    p.stdin.write(test_data.encode())
    ans = p.communicate()[0]
    if DEBUG:
        print(bytes.decode(ans))
    sock.send(ans)
    time.sleep(1)

receive = recv(sock)
sock.close()
