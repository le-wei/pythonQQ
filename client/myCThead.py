#!/usr/bin/python
import threading
import sys
import select,string
BUFSIZE =1024
class MyCThread(threading.Thread):
	def __init__(self,tcpClisSock):
		threading.Thread.__init__(self)
		self.tcpClisSock = tcpClisSock
	
		
	def run(self):
		Readline(self.tcpClisSock)


def Readline(tcpClisSock):
	print 'jjjjjjjjjjjjjjjjjjjjjjjjjjjj'
	while True:
		message=raw_input('fname::message>>')
		if message=='exit':
			tcpClisSock.send('exit')
			print 'you leave from chatroom'
			break
		else:
			num=message.find('::')
			if num==-1 or num==0:
				print'please input you friend name'
			else:
				tcpClisSock.send(message)
				sleep(0.5)