#!/usr/bin/env python
from socket import *
from time import ctime
import threading
from myconnect import *
from disposeMode import *
from operateDb import *
from myThead import *
HOST = ' 192.168.1.106'
PORT = 22222
BUFSIZE=1024
ADDR = (HOST,PORT)

tcpserverSock = socket(AF_INET,SOCK_STREAM)
tcpserverSock.bind(ADDR)
tcpserverSock.listen(5)

mutex = threading.Lock()
myconnect =  MyConnectDb()
DB_Session = myconnect.getSession()
while  True:
	try:
		print 'Waiting for connection'
		tcpCliSock,addr = tcpserverSock.accept()
		print 'connected from :',addr
		thread = MyThread(ServerLogic,tcpCliSock,DB_Session)
		thread.start()

	
	except KeyboardInterrupt:
		tcpserverSock.close()
		exit(1)
	