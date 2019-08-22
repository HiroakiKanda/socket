import MySQLdb

conn = MySQLdb.connect(user='socket_db_u', passwd='iisadmin', db='socket_db')
conn.autocommit(False)
cursor = conn.cursor()

try:
  cursor.execute('select * from t_door where door_no=1 and status=0')
  
  result = cursor.fetchall()
  print(result)

  cursor.execute('update t_door set status=1 where user_id='' and door_no=1 and status=0')
  conn.commit()

except Exception as e:
  conn.rollback()
  raise e

finally:
  cursor.close()
  conn.close()
