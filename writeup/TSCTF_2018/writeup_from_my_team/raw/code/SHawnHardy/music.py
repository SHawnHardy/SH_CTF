import socket
import time
import re

DEBUG = True

gap = 0.8

HOST, PORT = "10.112.82.102", int(4444)

ss = set(["named 'He Say'", "named 'See You Again'", "named 'I Hate You'", "named 'rolling in the deep'", "named 'They say'", "named 'honeysun'", "named 'God!'", "named 'Breakfast Is Delicious'", "named 'Bad Apple'", "named 'Butterfly'", "named 'Where Is My Shoes'", "named 'rolling'", "named 'Go'", "named 'I Mise You'", "named 'XiXiHaHa'", "named 'DuangDuangDuang'", "named 'Ga Li GayGay'", "named 'We don'", "named 'Just so so'", "named 'We dont talk any more'", "named 'zeshenprpr'", "named 'kidding'", "named 'Xiao Ping Guo'", "named 'I am a sheep'", "named 'Because of Love'", "named 'YiBao'", "named 'Zeshen is 666'", "named 'Misty Feels Xopowo'", "named 'Overthere'", "named 'Her say'", "named 'Overwatch'", "named 'LueLueLue'", "named 'XiXiXi'", "named 'Interesting'", "named 'Come on'", "named 'RuaRuaRua'", "named 'Just When I Needed You'", "named 'Good'"]);

ans = []

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    time.sleep(gap)

    recv = sock.recv(40960)
    if DEBUG:
        print(str(recv))



    while True:
        if not DEBUG and len(ans) > 2:
            print("".join(ans))
        try:
            song = re.findall("named '[\w\d !]*'", str(recv))
            # print(song[0])

            if song[0] in ss:
                sock.send(b"0")
                ans.append('0')
            else:
                sock.send(b"1")
                ans.append('1')

            time.sleep(gap)

            recv = sock.recv(40960)
            if DEBUG:
                print(str(recv))


            result = re.findall("NoNoNo", str(recv))
            # print(result)
            if len(result) > 0:
                ss.add(song[0])
                print(len(ss))
                break

            result = re.findall("{", str(recv))
            if len(result) > 0:
                print(str(recv))


        except socket.error:
            sock.close()
            break
        except IndexError:
            print(ss)
            print(str(recv))
            print("".join(ans))
            exit(0)
        # except KeyboardInterrupt:
        #     print(ss)
#

