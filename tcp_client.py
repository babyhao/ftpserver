from socket import *
import sys

sockfd = socket(AF_INET, SOCK_STREAM)

sockfd.connect(('0.0.0.0', 8888))

while True:
    try:
        data = input('Send>>')
        sockfd.send(data.encode())
        if data == '##':
            break
        data = sockfd.recv(1024).decode()
    except (KeyboardInterrupt, SystemError):
        sys.exit('客户端退出')
    print('Recive>>', data)

sockfd.close()