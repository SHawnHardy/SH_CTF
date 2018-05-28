import socket
import time
import re
import random

HOST, PORT = "10.112.108.77", int(1112)

DEBUG = True
GAP = 0.26


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


def get_map(receive):
    result = receive[(re.search(r"\s######################\s", receive).span()[0]):]
    result = result.split('\n')
    result = [list(x) for x in result]
    result = [x[-22:] for x in result]
    return result

def get_pos(mp):
    tpos = None
    for i in range(12):
        flag = False
        for j in range(22):
            if mp[i][j] == '@':
                tpos = (i, j)
                flag = True
                break
        if flag:
            break
    return tpos

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    time.sleep(GAP)

    receive = recv(sock)

    send(sock, "n")

    receive = recv(sock)

    send(sock, "")


    receive = recv(sock)
    lm = get_map(receive)
    lpos = get_pos(lm)

    send(sock, "step 1")
    receive = recv(sock)
    tm = get_map(receive)
    tpos = get_pos(tm)

    print(tpos)
    while True:
        if tpos[0] == 10:
            send(sock, "move " + str(tpos[1] - 1))
            recv(sock)
            if random.random() < 0.5:
                send(sock, "step 1")
            else:
                send(sock, "step 2")
        else:
            send(sock, "step " + str(10 - tpos[0]))
        receive = recv(sock)
        tm = get_map(receive)
        tpos = get_pos(tm)

sock.close()
