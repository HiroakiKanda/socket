# -*- coding:utf-8 -*-
# socket サーバを作成

import socket

# AF = IPv4 という意味
# TCP/IP の場合は、SOCK_STREAM を使う
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IPアドレスとポートを指定
s.bind(('127.0.0.1', 8982))
# 1 接続
s.listen(1)
# connection するまで待つ
while True:
    # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
    conn, addr = s.accept()
    while True:
        # データを受け取る
        data = conn.recv(1024)
        if not data:
            break
        print('data : {}, addr: {}'.format(data, addr))
        # クライアントにデータを返す(b -> byte でないといけない)
        conn.sendall(b'Received: ' + data)
