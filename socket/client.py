# -*- coding:utf-8 -*-
import socket

host = "172.31.92.113" #���g���̃T�[�o�[�̃z�X�g�������܂�
port = 8968 #�K����PORT���w�肵�Ă����܂�

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #�I�u�W�F�N�g�̍쐬�����܂�
client.connect((host, port)) #����ŃT�[�o�[�ɐڑ����܂�
client.send("Connect Client") #�K���ȃf�[�^�𑗐M���܂��i�͂����ɂ킩��悤�Ɂj


response = client.recv(4096) #���V�[�u�͓K����2�̗ݏ�ɂ��܂��i�傫������ƃ_���j
print response
