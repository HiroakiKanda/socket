# -*- coding:utf-8 -*-
import regex

#総受信データ分割クラス
class MyClass:
	def __init__(self, data):
		disassembledata = regex.split(b"",data, flags=regex.VERSION1)
		#最初と最後の'を消した配列を作成
		array=[]
		for item in disassembledata:
			if(len(item) > 0):
				array.append(item)
		#分解データをそれぞれの変数にセット
		#STX
		self.stx = array[0]
		#総データ長
		self.totaldatalength = array[1] + array[2]
		#送信先
		self.destination = array[3]
		#送信元
		self.sender = array[4]
		#予約エリア１
		self.reservearea1 = array[5]
		#暗号化区分
		self.cypherdivision = array[6]
		#予約エリア２
		self.reservearea2 = array[7]
		#シリアルNo
		self.serialno = array[8] + array[9]
		#アプリデータ長
		self.appdatalength = array[10] + array[11]
		#アプリデータ長の10進数（int型）
		self.intappdatalength = int.from_bytes(self.appdatalength,'big')
		#スペース
		self.space = array[12]
		#アプリデータ（配列）
		appdata_array = array[13:13+self.intappdatalength-1]
		#アプリデータ
		self.appdata = b''.join(appdata_array)
		#パディングデータ（配列）
		paddingdata_array = array[13+self.intappdatalength-1:-3]
		#パディングデータ
		self.paddingdata = b''.join(paddingdata_array)
		#ETX
		self.etx = array[-3]
		#予約エリア３
		self.reservearea3 = array[-2] + array[-1]

	def print_value(self):
		print('recv シリアルNo:' + str(self.serialno) + 'アプリデータ:' + str(self.appdata))


def disassemble(data):

	#データを全て分割して配列にする
	disassembledata = regex.split(b"",data, flags=regex.VERSION1)
	array=[]
	#最初と最後の'を消した配列を作成
	for item in disassembledata:
		if(len(item) > 0):
			array.append(item)

	#分割したデータから１行分のデータを取り出し、クラスを作成。
	offset=0
	returnarray=[]
	while(offset < len(array)):
		#総データ長取得
		totaldatalength = array[offset + 1] + array[offset + 2]
		#総データ長を10進数に変換
		inttotaldatalength = int.from_bytes(totaldatalength,'big')
		#オフセットから総データ長の値+3(「STX」と「総データ長」のデータ長)までを１行分のデータとする。
		splitdata = array[offset:offset + inttotaldatalength + 3]
		joindata = b''.join(splitdata)
		#クラスを作成し、返し用配列に追加
		returnarray.append(MyClass(joindata))
		#オフセットに1行分のデータ長を加算
		offset += len(joindata)


	return returnarray

def apdat_disassemble(data):

	#データを全て分割して配列にする
	disassembledata = regex.split(b"",data, flags=regex.VERSION1)
	array=[]
	#最初と最後の'を消した配列を作成
	for item in disassembledata:
		if(len(item) > 0):
			array.append(item)
	return array
