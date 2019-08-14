# -*- coding:utf-8 -*-
import time
from socket import socket, AF_INET, SOCK_DGRAM

HOST = ''
PORT = 8978
#ADDRESS = "172.31.92.113" # 自分に送信
ADDRESS = "127.0.0.1" # 自分に送信

s = socket(AF_INET, SOCK_DGRAM)
# ブロードキャストする場合は、ADDRESSを
# ブロードキャスト用に設定して、以下のコメントを外す
# s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

i = 0

while True:

    #msg = "close"
    msg = "Hello!! " + str(i)
    i += 1
    # 送信
    s.sendto(msg.encode(), (ADDRESS, PORT))
    time.sleep(3)

s.close()
