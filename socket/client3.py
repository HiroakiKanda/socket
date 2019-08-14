# -*- coding:utf-8 -*-
### -----------------------------------------------------------------------------------------------
#
#	処理概要		：
#	パラメータ	：
#	作成者			：
#	作成日			：
#
### -----------------------------------------------------------------------------------------------
import socket
import datetime
import binascii

## 接続情報
G_IP_ADDRESS='127.0.0.1'
G_PORT=8968
## シリアルNo
G_SERIAL_NO = 0x0000
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
		self.sock.sendall(msg.encode('utf-8'))
 
	def myreceive(self):
		dat = self.sock.recv(1024)
		print(dat)
		return dat

### 10進数を2バイト16進数に変換
def hex_fomat(dat):
	quotient,remainder = divmod(dat,256)
	return hex(quotient) + hex(remainder)
        
### 通信フォーマット作成
def make_fmt( cmd_type, auth_dat ):
	global G_SERIAL_NO
	# アプリデータ
	if cmd_type == 0:			# 通知保持
		fmt_app = '\x00'
	elif cmd_type == 1:		# 起動通知
		fmt_app = '\x01' 
	elif cmd_type == 3:		# 認証要求
		fmt_app = '\x03\x00\x00' + 'face' + auth_dat
	else:
		return None
    	
	# スペース
	fmt_spc='\x20'
	# アプリデータ長
	fmt_app_dat = fmt_spc + fmt_app
	fmt_app_len = hex_fomat(len(fmt_app_dat))
	print('fmt_app_len=' + fmt_app_len)
	
	# 送信先、送信元、予約エリア１、暗号化区分、予約エリア２
	fmt_start='\x00\x00\x00\x00\x00'
	# シリアルNo
	fmt_serial= hex_fomat(G_SERIAL_NO)
	print('fmt_serial=' + fmt_serial)
	
	# 総データ長
	fmt_all_dat=fmt_start + fmt_serial + fmt_app_len + fmt_app_dat
	print('fmt_all_dat=' + fmt_all_dat)
	
	fmt_all_len= hex_fomat(len(fmt_all_dat))
	print('fmt_all_len=' + fmt_all_len)

	# STX
	fmt_stx='\x02'		
	# ETX
	fmt_etx='\x03'
	# 予約エリア３
	fmt_end='\x00\x00'
	
	fmt_dat = fmt_stx + fmt_all_len + fmt_all_dat + fmt_etx + fmt_end
	print('fmt_dat=' + fmt_dat)
	
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
	serial_no_cnt()

	mysock.mysend(send_dat)
	recv_dat=mysock.myreceive()

	#インターバル時間設定
	previous_time = datetime.datetime.now()
	print(previous_time)
	interval = datetime.timedelta(seconds=60)

	### 要求確認
	while True:
		current_time = datetime.datetime.now()
		if  (previous_time + interval < current_time):
			previous_time = current_time
			print(previous_time)

			### 通信保持
			send_dat = make_fmt(0, None)		
			print(send_dat)
			serial_no_cnt()
			mysock.mysend(send_dat)
			recv_dat=mysock.myreceive()
			### タブレットから要求あり
	