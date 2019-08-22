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
import time

## 接続情報
G_IP_ADDRESS='172.31.92.123'
#G_IP_ADDRESS='127.0.0.1'
G_PORT=8983
## シリアルNo
G_SERIAL_NO = 0
G_MAX_SERIAL_NO = 32767
G_RECV_SIZE = 2048

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
		dat = self.sock.recv(G_RECV_SIZE)
		print('受信 recv->')
		print(dat)
		return dat

        def close(self):
                self.sock.close()

### 10進数を2バイトでビッグエンディアンに変換
def hex_fomat(dat):
	ret_cd=dat.to_bytes(2,'big')
	return ret_cd

### 通信フォーマット作成
def make_fmt( cmd_type, auth_dat ):
	global G_SERIAL_NO
	# アプリデータ
	if cmd_type == 0:			# 通知保持
		fmt_app = b'\x00'
	elif cmd_type == 1:			# 起動通知
		fmt_app = b'\x01\x01' 
	elif cmd_type == 3:			# 認証要求
		fmt_auth_len = len('face' + auth_dat).to_bytes(1,'big')
		fmt_app = b'\x03\x00\x00' + fmt_auth_len + bytes('face' + auth_dat, 'utf-8')
	else:
		return None
   	
	# スペース
	fmt_spc=b'\x20'
	# アプリデータ長
	fmt_app_dat = fmt_spc + fmt_app
	fmt_app_len = hex_fomat(len(fmt_app_dat))
	print('アプリデータ')
	print(fmt_app_dat)
	
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
	#print('送信電文')
	#print(fmt_dat)
	
	return fmt_dat

### シリアルNOカウント
def serial_no_cnt():
	global G_SERIAL_NO
	global G_MAX_SERIAL_NO
	
	if G_SERIAL_NO == G_MAX_SERIAL_NO:
		G_SERIAL_NO = 0
	else:
		G_SERIAL_NO += 1

if __name__=='__main__':
	
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
	print(previous_time2)
	interval = datetime.timedelta(seconds=60)
	interval2 = datetime.timedelta(seconds=20)

	### 要求確認
	while True:
		current_time = datetime.datetime.now()
		if  (previous_time + interval < current_time):
			previous_time = current_time
			print('previous_time')
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
			print('previous_time2')
			print(previous_time2)
	
			### 認証要求
			send_dat = make_fmt(3, 'iis70109')
			print('認証要求 send->')
			print(send_dat)
			serial_no_cnt()
			mysock.mysend(send_dat)
			recv_dat=mysock.myreceive()
		else:
			time.sleep(1)	
			recv_dat=mysock.myreceive()

	mysock.close()

