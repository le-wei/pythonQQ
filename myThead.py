#!/usr/bin/python
import threading
from disposeMode import *

class MyThread(threading.Thread):
	def __init__(self,func,TcpScoket,DB_Session):
		threading.Thread.__init__(self)
		self.TcpScoket = TcpScoket
		self.func = func
		self.DB_Session = DB_Session
	
		
	def run(self):
		ServerLogic(self.TcpScoket,self.DB_Session)



		