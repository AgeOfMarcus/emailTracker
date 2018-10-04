#!/usr/bin/python3

from flask import Flask, request, send_file
from termcolor import colored
from uuid import uuid4
import json, time, fire

##### SETTINGS #####

debug_to_console = True # log debug messages to console
debug_to_file = True # log debug messages to a file called 'debug_log.txt'

##### SETTINGS #####

# debugging
def debug(*args):
	if debug_to_console:
		for i in args:
			print("[DEBUG] : "+i)
	if debug_to_file:
		try:
			with open("debug_log.txt","a") as f:
				for i in args:
					f.write(i)
		except Exception as e:
			with open("debug_log.txt","w") as f:
				f.write(alert("Error writing to debug file, creating..."))
				for i in args:
					f.write(i)

# coloured messages
def alert(msg): return colored("[!] ","red") + msg
def info(msg): return colored("[*] ","cyan") + msg
def plus(msg): return colored("[+] ","green") + msg
def minus(msg): return colored("[-] ","blue") + msg

# importing previous clients
def clients():
	try:
		return json.loads(open("clients.json","r").read())
	except Exception as e:
		debug(alert("Error importing clients from clients.json: "+e))
		try:
			a = open("clients.json","r").read()
			debug(info("File is readable, json must be corrupt"))
			debug(info("Wiping clients.json, old data can be found in old.clients.json"))
			with open("old.clients.json","w") as f:
				f.write(a)
			b = open("clients.json","w").close()
			return {}
		except:
			debug(alert("File appears to not exist, creating..."))
			a = open("clients.json","w").close()
			return {}
# adding new clients to the file
def add_client(uuid, nick=None):
	old = clients()
	old[uuid] = {'nick':nick,'timestamps':[],'hits':0,'hosts':{}}
	with open("clients.json","w") as f:
		f.write(json.dumps(old))


# flask server

app = Flask(__name__)

@app.route("/images/<uuid>/<image_name>")
def send_image(uuid, image_name):
	ts = time.time()
	cl = clients()
	if not uuid in cl:
		debug(alert("Unknown uuid [%s] attempted to access image [%s] at timestamp: %s" % (uuid,image_name,str(ts))))
		return "", 404
	else:
		cl[uuid]['timestamps'].append(ts)
		cl[uuid]['hits'] += 1
		cl[uuid]['hosts'][ts] = request.remote_addr
		debug(plus("We got a hit from client [%s] (ip: %s) at timestamp: %s" % (uuid,request.remote_addr,str(ts))))
		with open("clients.json","w") as f:
			f.write(json.dumps(cl))
		return send_file("blank_pixel.png", mimetype="image/gif")


class CLI(object):
	def run(self, ip, port):
		app.run(host=ip, port=int(port))
	def addClient(self, nickname):
		add_client(str(uuid4()),nickname)
if __name__ == "__main__":
	fire.Fire(CLI)