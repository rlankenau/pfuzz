#!/usr/bin/python
import SocketServer
from optparse import OptionParser
import subprocess
import sys
import signal, os

server = None
shutdown = False
process = None
cmd = None

class PFuzzServerHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		global process,cmd
		data = self.request[0].strip()
		if (data == 'START'):
			print "Starting process %s"%(" ".join(cmd))
			process = subprocess.Popen(" ".join(cmd), shell=True)
		elif(data == 'STOP'):
			if(process != None and process.poll() == None):
				print "Stopping process"
				process.send_signal(signal.SIGINT)
				if(process.poll() == None):
					print "Failed to stop process."
			else :
				print "Process is not running"
		elif(data == 'STATUS'):
			self.send_status(self.client_address)
		elif(data == 'INFO'):
			self.send_info(self.client_address)

	def send_status(self, client):
		global process
		socket = self.request[1]
		if(process != None and process.poll() == None) :
			socket.sendto("RUNNING", client)
		else :
		 	socket.sendto("STOPPED", client)

	def send_info(self, client):
		global process
		socket = self.request[1]
		socket.sendto("Not Implemented", client)

if __name__ == "__main__":
	parser = OptionParser(usage="Control a process, and provide information about its status.")
	parser.disable_interspersed_args()
	(options, args) = parser.parse_args()

	HOST, PORT = "localhost", 0
	cmd = args
	server = SocketServer.UDPServer((HOST,PORT), PFuzzServerHandler)
	print "Server listening on %s:%d"%(server.server_address)
	server.timeout=1
	while shutdown == False:
		server.handle_request()
