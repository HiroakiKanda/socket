#! /usr/bin/env python
import subprocess
import sys

command = ["pkill", "-f", "udpsend.py"]
try:
	res = subprocess.check_call(command)
	print("check_call() result: " + str(res))
except:
	print("subprocess.subprocess.check_call() failed")

command = ["python3", "udpsend.py"]
try:
        res = subprocess.Popen(command)
        print("Popen() result: " + str(res))
except:
        print("subprocess.subprocess.Popen() failed")
