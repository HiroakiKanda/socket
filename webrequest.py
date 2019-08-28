# -*- coding:utf-8 -*-

import argparse
import json
import MySQLdb
import logging
import cgi

from http.server import BaseHTTPRequestHandler, HTTPServer

socketdb = 'socket_db'
socketuser = 'socket_db_u'
socketpasswd = 'iisadmin'

def selectDb(sql, param):
    connection = MySQLdb.connect(db=socketdb, user=socketuser, passwd=socketpasswd)
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql, param)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def execDb(sql, param):
    connection = MySQLdb.connect(db=socketdb, user=socketuser, passwd=socketpasswd)
    cursor = connection.cursor()
    cursor.execute(sql, param)
    connection.commit()
    cursor.close()
    connection.close()

class MyHandler(BaseHTTPRequestHandler):
    """
    Received the request as json, send the response as json
    please you edit the your processing
    """
    def do_POST(self):
        try:
            content_len=int(self.headers.get('content-length'))

            requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))

            logging.info('recv user_id:' + requestBody['user_id'] + ' door_no:' + requestBody['door_no'])	

            insertjson = {}
            insertsql = ('insert into t_door (user_id, door_no, status) values(%(user_id)s, %(door_no)s, "0")')
            insertjson['user_id'] = requestBody['user_id']
            insertjson['door_no'] = requestBody['door_no']
            execDb(insertsql,insertjson)

            response = { 'status' : 200 }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)

            self.wfile.write(responseBody.encode('utf-8'))
        except Exception as e:
            print("An error occured")
            print("The information of error is as following")
            print(type(e))
            print(e.args)
            print(e)
            response = { 'status' : 500 }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)

            self.wfile.write(responseBody.encode('utf-8'))

def importargs():
    parser = argparse.ArgumentParser("This is the simple server")

    parser.add_argument('--host', '-H', required=False, default='localhost')
    parser.add_argument('--port', '-P', required=False, type=int, default=8080)

    args = parser.parse_args()

    return args.host, args.port

def run(server_class=HTTPServer, handler_class=MyHandler, server_name='localhost', port=8080):

    server = server_class(('', port), handler_class)
    server.serve_forever()

def main():
    host, port = importargs()
    run(server_name=host, port=port)

if __name__ == '__main__':
    formatter = '%(levelname)s : %(asctime)s : %(message)s'
    logging.basicConfig(filename='logs/webrequest.log', level=logging.INFO, format=formatter)
    main()
