# -*- coding:utf-8 -*-
# socket �T�[�o���쐬

import socket

# AF = IPv4 �Ƃ����Ӗ�
# TCP/IP �̏ꍇ�́ASOCK_STREAM ���g��
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IP�A�h���X�ƃ|�[�g���w��
s.bind(('127.0.0.1', 8982))
# 1 �ڑ�
s.listen(1)
# connection ����܂ő҂�
while True:
    # �N�����A�N�Z�X���Ă�����A�R�l�N�V�����ƃA�h���X������
    conn, addr = s.accept()
    while True:
        # �f�[�^���󂯎��
        data = conn.recv(1024)
        if not data:
            break
        print('data : {}, addr: {}'.format(data, addr))
        # �N���C�A���g�Ƀf�[�^��Ԃ�(b -> byte �łȂ��Ƃ����Ȃ�)
        conn.sendall(b'Received: ' + data)
