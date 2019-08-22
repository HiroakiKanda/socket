# -*- coding:utf-8 -*-
from socket import socket, AF_INET, SOCK_DGRAM

HOST = ''
PORT = 8978

# ソケットを用意
s = socket(AF_INET, SOCK_DGRAM)
# バインドしておく
s.bind((HOST, PORT))

while True:
	try:
	# 受信
		msg, address = s.recvfrom(8192)
		print(msg)
		if msg == 'close':
		#受信した文字列がcloseならUDPソケットを閉じて終了
			s.close()
			break
	except KeyboardInterrupt:
		#強制終了を検知したらUDPソケットを閉じて終了
		s.close()

