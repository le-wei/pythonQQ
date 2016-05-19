#!/usr/bin/env python
from socket import *
from time import ctime
import threading
from myconnect import *
from disposeMode import *
from operateDb import *
from myThead import *
HOST = ' 192.168.1.103'
PORT = 22222
BUFSIZE=1024
ADDR = (HOST,PORT)

tcpserverSock = socket(AF_INET,SOCK_STREAM)
tcpserverSock.bind(ADDR)
tcpserverSock.listen(5)

Online= {}
Mutex = threading.Lock()
myconnect =  MyConnectDb()


while  True:
	try:
		print 'Waiting for connection'
		tcpCliSock,addr = tcpserverSock.accept()
		DB_Session = myconnect.getSession()
		print 'connected from :',addr
		thread = MyThread(ServerLogic,tcpCliSock,DB_Session,Mutex,Online)
		thread.start()

	
	except KeyboardInterrupt:
		tcpserverSock.close()
		exit(1)
	
