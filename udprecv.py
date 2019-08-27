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
import logging

from importdir import disassemble
from socket import socket, AF_INET, SOCK_DGRAM

HOST = ''
PORT = 8978

# ソケットを用意
s = socket(AF_INET, SOCK_DGRAM)
# バインドしておく
s.bind((HOST, PORT))

## ログ設定
formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(filename='logs/udprecv.log', level=logging.INFO, format=formatter)

## 受信開始　無限ループ
while True:
	try:
	# 受信
		msg, address = s.recvfrom(1024)
		logging.info(msg)

		time.sleep(0.5)
		recv_dat = disassemble.disassemble(msg)
		for member in recv_dat:
			logging.info('recv シリアルNo:' + str(member.serialno) + 'アプリデータ:' + str(member.appdata))	
			app_array = disassemble.apdat_disassemble(member.appdata)

			### 接続要求受信	
			if app_array[0] == b'\xc8':
				str_key=''
				for i in range(4):
					str_key = str_key + app_array[i+1].decode('utf-8')
				logging.info(str_key)		

				str_cmd = 'tcpsock' + str_key + '.py'
				logging.info(str_cmd)

				command = ["pkill", "-f", str_cmd]
				try:
					res = subprocess.check_call(command)
					logging.info("check_call() result: " + str(res))
				except:
					logging.info("subprocess.subprocess.check_call() failed")

				command = ["python3", str_cmd]
				logging.info(command)
				try:
					res = subprocess.Popen(command)
					logging.info("Popen() result: " + str(res))
				except:
					logging.info("subprocess.subprocess.Popen() failed")

	except KeyboardInterrupt:
		#強制終了を検知したらUDPソケットを閉じて終了
		s.close()
