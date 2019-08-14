from struct import *

data = pack('h', 1)

#print(type(data))
#print(data)

a = 128

fmt_app = b'\x01' 
fmt_spc=b'\x20'
fmt_app_dat = fmt_spc + fmt_app
fmt_app_len = len(fmt_app_dat)

#print(fmt_app_dat)
#print(fmt_app_len)
#print(fmt_app_len.to_bytes(2,'big'))

# 2バイトでビッグエンディアン
#print('a=' + a.to_bytes(2, 'big').decode('utf-8') ) 

# 4バイトでリトルエンディアン
#print(a.to_bytes(4, 'little')  )

message = 'こんにちは、Pythonプログラミング'
print(bytes(message, 'UTF-8') )
# messageをUTF-8コードのバイト列に変換(エンコード)する。
