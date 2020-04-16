from socket import *
from threading import Thread
from time import sleep
import sys
HOST = "127.0.0.1"
PORT = 8888
ADDR = (HOST, PORT)
FTP = "/home/tarena/File/"

class FTPSever(Thread):
    def __init__(self,connfd):
        super().__init__()
        self.connfd = connfd

    def do_list(self):


    def run(self):
        data = self.connfd.recv(1024).decode()
        if not data or data == "E":
            return
        elif data == "L":
            do_list()


def main():
    s = socket()
    s.bind(ADDR)
    s.listen(3)
    print("Listen the port 8888")
    try:
        connfd,addr = s.accept()
        print("客户端地址:",addr)
    except:
        sys.exit("服务端退出")

    t = FTPSever(connfd)
    t.daemon = True
    t.start()

