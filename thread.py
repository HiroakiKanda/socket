#!/usr/bin/python3

import threading
import time

def hello(thr_no):
  time.sleep(2.5)
  print(thr_no)

def hello1():
  t = threading.Timer(3, hello1)
  t.start()
  hello("hello1")

def hello2():
  while True:
    time.sleep(3)
    hello("hello2")

if __name__=='__main__':
  t1 = threading.Thread(target=hello1)
  t1.start()
  t2 = threading.Thread(target=hello2)
  t2.start()