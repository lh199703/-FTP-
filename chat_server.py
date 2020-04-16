from socket import *
from multiprocessing import Process
ADDR = ("0.0.0.0", 8888)

user = {}
# 用户进入聊天室
def do_loding(s,name,address):
    if name in user or "管理" in name:
        s.sendto("用户名已存在".encode(), address)
        return
    else:
        s.sendto(b"OK", address)
        msg = "\n欢迎%s进入了聊天室" % name
        for i in user:
            s.sendto(msg.encode(), user[i])
        user[name] = address

def do_chat(s,name,text):
    msg = "\n%s : %s" % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])

def do_quit(s,name):
    del user[name]
    for i in user:
        msg = "\n%s退出了聊天室" % name
        s.sendto(msg.encode(), user[i])

def request(s):
    while True:
        data, addr = s.recvfrom(1024)
        tmp = data.decode().split(" ",2)
        if tmp[0] == "L":
            do_loding(s, tmp[1], addr)
        elif tmp[0] == "C":
            do_chat(s, tmp[1], tmp[2])
        elif tmp[0] == "Q":
            do_quit(s, tmp[1])

def manager(s):
    while True:
        msg = input("管理员消息:")
        msg = "C 管理员 " + msg
        s.sendto(msg.encode(), ADDR)

def main():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    p = Process(target=request,args=(s,))
    p.start()
    manager(s)
    p.join()


if __name__ == '__main__':
    main()