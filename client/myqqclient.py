#!/usr/bin/env python
from socket import *
import sys
from time import sleep
import select,string
from shouface import *
from myCThead import *
sign = False
resum=0
HOST='192.168.1.103'
PORT=22222
BUFSIZE=1024
ADDR=(HOST,PORT)
try:
	tcpClisSock = socket(AF_INET,SOCK_STREAM)
	tcpClisSock.connect(ADDR)
except Exception:
	print 'Connect is error'
	sys.exit()

while True:
	try:
		if not sign:
			showLOI()
			instruct=raw_input('input your instruct 1 or 2 >>')
			if not instruct in ('1','2'):
				print instruct
				print 'please input you instruct 1 or 2'
				continue
			else:
				if instruct=='1' and resum==0:
					tcpClisSock.send('1')
					renum=Login(tcpClisSock)
					if renum==1:
						sign=True
						continue
					elif renum==2:
						print 'you shourd to register'
						resum = 3
						continue
					elif renum==3:
						tcpClisSock.send('exit')
						print 'sercer sql is error you must waiting'
						tcpClisSock.close()
						sys.exit()
				elif instruct=='1' and resum == 3:
					print 'you must not login ,you can register'
					continue
				if instruct=='2':
					tcpClisSock.send('2')
					renum=Register(tcpClisSock)
					if renum==1:
						print 'you regist is ok,you can login'
						continue
					elif renum== 2:
						print 'you exit regist,you can login'
						continue
					elif renum==3:
						tcpClisSock.send('exit')
						print 'sercer sql is error you must waiting'
						tcpClisSock.close()
						sys.exit()
		elif sign:
			showOperater()
			instruct=raw_input('input your instruct >>')
			if not instruct in ('3','4','5','6','7','exit','quit'):
				print 'you input is error ,please again'
				continue
			elif instruct=='3':
				print'3333333333333'
				tcpClisSock.send('3')
				renum=chatFriend(tcpClisSock)
				if renum==1:
					print 'you leave from chatroom'
					continue
				elif renum==2:
					print'you must to add friend'
					continue
			elif instruct=='4':
				tcpClisSock.send('4')
				renum=andfriend(tcpClisSock)
				if renum==3:
					tcpClisSock.send('exit')
					print 'sercer sql is error you must waiting'
					tcpClisSock.close()
					sys.exit()
				elif renum==1:
					print'you andfriend is ok'
					continue
				elif renum==2:
					print'Sorry,Do not have your friend'
					continue
			elif instruct=='5':
				tcpClisSock.send('5')
				renum = deletefriend(tcpClisSock)
				if renum==3:
					tcpClisSock.send('exit')
					print 'sercer sql is error you must waiting'
					tcpClisSock.close()
					sys.exit()
				elif renum==1:
					print 'delete is ok'
					continue
				elif renum==2:
					print 'you can select  other'
					continue
			elif instruct in (6,7):
				print 'Sorry,this cant not use'
				continue
			elif instruct == 'quit':
				print 'you will log out after 2 second'
				sign=False
				sleep(2)
				continue
			elif instruct=='exit':
				tcpClisSock.send('exit')
				print 'you will go out from System'
				tcpClisSock.close()
				exit(1)
	except KeyboardInterrupt:
		tcpClisSock.send('exit')
		print'Bey'
		tcpClisSock.close()
		exit(1)

