# -*- coding:utf-8 -*-
### -----------------------------------------------------------------------------------------------
#
#       処理概要        ： TCP Socket
#       パラメータ      ：
#       作成者          ： IIS H.Kanda
#       作成日          ： 2019/08
#
### -----------------------------------------------------------------------------------------------
import socket
import datetime
import argparse
import json
import cgi

from multiprocessing import Queue, Process
from http.server import BaseHTTPRequestHandler, HTTPServer

## 接続情報
#G_IP_ADDRESS='172.31.92.123'
G_IP_ADDRESS='127.0.0.1'
G_PORT=8982
## シリアルNo
G_SERIAL_NO = 0
G_MAX_SERIAL_NO = 32767

## Socket通信クラス
class MySocket:
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
			
	def connect(self, host, port):
		self.sock.connect((host, port))

	def mysend(self, msg):
		#self.sock.sendall(msg.encode('utf-8'))
		self.sock.sendall(msg)

	def myreceive(self):
		dat = self.sock.recv(2048)
		print(dat)
		return dat

### 10進数を2バイトでビッグエンディアンに変換
def hex_fomat(dat):
#	quotient,remainder = divmod(dat,256)
#	ret_cd = hex(quotient) + hex(remainder)
	ret_cd=dat.to_bytes(2,'big')
	return ret_cd

### 通信フォーマット作成
def make_fmt( cmd_type, auth_dat ):
	global G_SERIAL_NO
	# アプリデータ
	if cmd_type == 0:			# 通知保持
		fmt_app = b'\x00'
	elif cmd_type == 1:			# 起動通知
		fmt_app = b'\x01' 
	elif cmd_type == 3:			# 認証要求
		fmt_app = b'\x03\x00\x00' + bytes('face' + auth_dat,  'UTF-8')
	else:
		return None
   	
	# スペース
	fmt_spc=b'\x20'
	# アプリデータ長
	fmt_app_dat = fmt_spc + fmt_app
	fmt_app_len = hex_fomat(len(fmt_app_dat))
	print('アプリデータ長')
	print(fmt_app_len)
	
	# 送信先、送信元、予約エリア１、暗号化区分、予約エリア２
	fmt_start=b'\x00\x00\x00\x00\x00'
	# シリアルNo
	fmt_serial= hex_fomat(G_SERIAL_NO)
	print('シリアルNo')
	print(fmt_serial)
	
	# 総データ長
	fmt_all_dat=fmt_start + fmt_serial + fmt_app_len + fmt_app_dat
	print('総データ電文')
	print(fmt_all_dat)
	
	fmt_all_len= hex_fomat(len(fmt_all_dat))
	print('総データ長')
	print(fmt_all_len)

	# STX
	fmt_stx=b'\x02'		
	# ETX
	fmt_etx=b'\x03'
	# 予約エリア３
	fmt_end=b'\x00\x00'
	
	fmt_dat = fmt_stx + fmt_all_len + fmt_all_dat + fmt_etx + fmt_end
	print('送信電文')
	print(fmt_dat)
	
	return fmt_dat

### シリアルNOカウント
def serial_no_cnt():
	global G_SERIAL_NO
	global G_MAX_SERIAL_NO
	
	if G_SERIAL_NO == G_MAX_SERIAL_NO:
		G_SERIAL_NO = 0
	else:
		G_SERIAL_NO += 1

### WEBサーバー処理
class MyHandler(BaseHTTPRequestHandler):
	def do_POST(self):

		try:
			content_len=int(self.headers.get('content-length'))
			requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))

			print(requestBody)

			res = {}
			for key in requestBody:
				res[key] = requestBody[key]
			response = { 'status' : 200, 'result' : res}
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			responseBody = json.dumps(response)
			self.wfile.write(responseBody.encode('utf-8'))
		except Exception as e:
			print("An error occured")
			print("The information of error is as following")
			print(type(e))
			print(e.args)
			print(e)
			response = { 'status' : 500, 'msg' : 'An error occured' }
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			responseBody = json.dumps(response)
			self.wfile.write(responseBody.encode('utf-8'))

if __name__=='__main__':
	
	### WEBサーバー起動
#	webhost, webport = importargs()
	server_class=HTTPServer
	handler_class=MyHandler
	server_name=''
	port=8080
	server = server_class((server_name, port), handler_class)
	server_process = Process(target=server.serve_forever)
	server_process.daemon = True
	server_process.start()

	### 接続確立	
	mysock = MySocket()
	mysock.connect(G_IP_ADDRESS,G_PORT)

	### 接続通知
	send_dat = make_fmt(1, None)
	print('起動通知 send->' )
	print(send_dat)
	serial_no_cnt()

	mysock.mysend(send_dat)
	recv_dat=mysock.myreceive()

	#インターバル時間設定
	previous_time = datetime.datetime.now()
	previous_time2 = datetime.datetime.now()
	print(previous_time)
	interval = datetime.timedelta(seconds=60)
	interval2 = datetime.timedelta(seconds=20)

	### 要求確認
	while True:
		current_time = datetime.datetime.now()
		if  (previous_time + interval < current_time):
			previous_time = current_time
			print(previous_time)

			### 通信保持
			send_dat = make_fmt(0, None)		
			print('通信保持 send->' )
			print(send_dat)
			serial_no_cnt()
			mysock.mysend(send_dat)
			recv_dat=mysock.myreceive()

		elif (previous_time2 + interval2 < current_time):	
			previous_time2= current_time
	
			### 認証要求
			send_dat = make_fmt(3, 'ais70109')
			print('認証要求 send->')
			print(send_dat)
			serial_no_cnt()
			mysock.mysend(send_dat)
			recv_dat=mysock.myreceive()

	server_process.terminate()
	