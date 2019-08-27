# -*- coding:utf-8 -*-
### -----------------------------------------------------------------------------------------------
#
#       処理概要        ： UDP通知を受信したらプロセスを再起動する
#       パラメータ      ：
#       作成者          ： IIS H.Kanda
#       作成日          ： 2019/08
#
### -----------------------------------------------------------------------------------------------
import subprocess
import sys
import time

from importdir import disassemble
from socket import socket, AF_INET, SOCK_DGRAM

HOST = ''
PORT = 8978

# ソケットを用意
s = socket(AF_INET, SOCK_DGRAM)
# バインドしておく
s.bind((HOST, PORT))

## 受信開始　無限ループ
while True:
	try:
	# 受信
		msg, address = s.recvfrom(1024)
		print(msg)

		time.sleep(0.5)
		recv_dat = disassemble.disassemble(msg)
		for member in recv_dat:
			print('recv シリアルNo:' + str(member.serialno) + 'アプリデータ:' + str(member.appdata))	
			app_array = disassemble.apdat_disassemble(member.appdata)

			### 接続要求受信	
			if app_array[0] == b'\xc8':
				str_key=''
				for i in range(4):
					str_key = str_key + app_array[i+1].decode('utf-8')
				print(str_key)		

				str_cmd = 'otest' + str_key + 'v3.py'
				print(str_cmd)

				command = ["pkill", "-f", str_cmd]
				try:
					res = subprocess.check_call(command)
					print("check_call() result: " + str(res))
				except:
					print("subprocess.subprocess.check_call() failed")

				command = ["python3", str_cmd]
				print(command)
				try:
					res = subprocess.Popen(command)
					print("Popen() result: " + str(res))
				except:
					print("subprocess.subprocess.Popen() failed")

	except KeyboardInterrupt:
		#強制終了を検知したらUDPソケットを閉じて終了
		s.close()
