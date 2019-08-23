import MySQLdb

mydb = 'socket_db'
myuser = 'socket_db_u'
mypasswd = 'iisadmin'

def selectDb(sql):
    connection = MySQLdb.connect(db=mydb, user=myuser, passwd=mypasswd)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def execDb(sql):
    connection = MySQLdb.connect(db=mydb, user=myuser, passwd=mypasswd)
    connection.autocommit(False)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
