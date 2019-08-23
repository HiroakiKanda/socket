# -*- coding:utf-8 -*-
import MySQLdb
from time import sleep

if __name__=='__main__':

	myconn = MySQLdb.connect(user='socket_db_u', passwd='iisadmin', db='socket_db')
	myconn.autocommit(True)
	mycursor = myconn.cursor()

	sel_dat = "select user_id,door_no from t_door"
	sel_dat = sel_dat + " where user_id = 'iis70213' and status='0' FOR UPDATE"

	while True:
		try:

			mycursor.execute(sel_dat)
			recv_dbs = mycursor.fetchall()
			print(recv_dbs)
			sleep(10)

		except Exception as e:
			myconn.rollback()
			raise e

	mycursor.close()
	myconn.close()