from socket import *
import os
import sys
import signal
import time

# 文件库路径
FILE_PATH = '/home/tarena/mydict/'

HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)


# 封装文件服务器的功能：获取文件列表、下载文件、上传文件
class FtpServer:
    def __init__(self, c):
        self.c = c

    # 获取文件列表
    def do_list(self):
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.c.send('文件库为空'.encode())
            return
        else:
            self.c.send(b'OK')
            time.sleep(0.1)

        files = ''
        for file in file_list:
            if (file[0] != '.') and os.path.isfile(FILE_PATH + file):
                files += file + '#'
        self.c.send(files.encode())

    # 下载文件
    def do_get(self, filename):
        try:
            f = open(FILE_PATH + filename, 'rb')
        except:
            self.c.send('文件不存在'.encode())
            return

        self.c.send(b'OK')
        time.sleep(0.1)

        while True:
            msg = f.read(1024)
            if not msg:
                time.sleep(0.1)
                self.c.send(b'##')
                break
            self.c.send(msg)
        print('文件发送完毕')
        f.close()

    # 上传文件
    def do_put(self, filename):
        try:
            f = open(FILE_PATH + filename, 'wb')
        except:
            print('文件打开失败')

        self.c.send(b'OK')
        while True:
            msg = self.c.recv(1024)
            if msg == b'##':
                break
            f.write(msg)
        print('文件上传完毕')
        f.close()


# 处理客户端请求
def client_handler(c):
    ftp = FtpServer(c)
    while True:
        msg = c.recv(1024).decode()
        if not msg or msg[0] == 'Q':
            c.close()
            sys.exit('客户端退出')
        elif msg[0] == 'L':
            ftp.do_list()
        elif msg[0] == 'G':
            filename = msg.split(' ')[-1]
            ftp.do_get(filename)
        elif msg[0] == 'P':
            filename = msg.split(' ')[-1]
            ftp.do_put(filename)
        else:
            c.send(b'Invalid choice')


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        print('Processing-%d waiting for connect...' % os.getpid())
        c, addr = s.accept()
        print('Connect from', addr)

        pid = os.fork()
        if pid == 0:
            s.close()
            client_handler(c)
        else:
            c.close()


if __name__ == '__main__':
    main()
