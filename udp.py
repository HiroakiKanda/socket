import socket #通信用

#通信を受け付けるIPアドレスと受信に使うポート番号の設定．127.0.0.1とするとPC内通信．
address = ('127.0.0.1', 8978) 

#udpという名前のUDPソケット生成
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#udpというソケットにaddressを紐づける
udp.bind(address) 

#受信ループ
while True: 
    try:
        rcv_byte = bytes() 
        #バイトデータ受信用変数
        rcv_byte, addr = udp.recvfrom(1024) 
        #括弧内は最大バイト数設定
        msg = rcv_byte.decode() 
        #バイトデータを文字列に変換
        print(msg) 
        #文字列表示
        if msg == 'close': 
        #受信した文字列がcloseならUDPソケットを閉じて終了
            udp.close()
            break
    except KeyboardInterrupt:
    	#強制終了を検知したらUDPソケットを閉じて終了
        udp.close()