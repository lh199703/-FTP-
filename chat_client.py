from socket import *
from multiprocessing import Process
import sys
ADDR = ("127.0.0.1", 8888)

def recv(s):
    while True:
        data,addr = s.recvfrom(1024)
        print(data.decode(), "\n发言:", end="")



def send(s,name):
    while True:
        try:
            text = input("\n发言:")
        except KeyboardInterrupt:
            text = "quit"
        if text == "quit":
            msg = "Q "+name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入昵称:")
        msg = "L "+name
        s.sendto(msg.encode(), ADDR)
        data,addr = s.recvfrom(128)
        if data.decode() == "OK":
            print("您已进入聊天室")
            break
        else:
            print(data.decode())
    p = Process(target=recv, args=(s,))
    p.daemon = True
    p.start()
    send(s, name)


if __name__ == '__main__':
    main()