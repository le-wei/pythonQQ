#!/usr/bin/env python
import sys
import select
from time import sleep
from myCThead import *
BUFSIZE=1024
def showLOI():
	print '============================================'
	print '============================================'
	print '==== 1:Log In System             2:Regist User ========='
	print '============================================'
	print '============================================'

def showOperater():
	print '======================================================='
	print '======================================================='
	print '=====3:Chat Witch Friend        4:Add Friend==================='
	print '=====5:Delete Friend                 6:Create  Tribe=================='
	print '=====7:Chat Witch Friends      \'quit\':log out==================='
	print '==========    \'exit\':Go Out From System====================='
	print '======================================================='
	print '======================================================= '

def Login(tcpClisSock):
	num=0
	while  True :
		print num
		if num >2:
			tcpClisSock.send('exit')
			return 2
		rlist = [sys.stdin,tcpClisSock]
		read_list,write_list,error_list=select.select(rlist,[],[],0.2)
		if tcpClisSock in read_list:
			remessage=tcpClisSock.recv(BUFSIZE)
			if remessage=='Loginok':
				return 1
			elif remessage=='sqlerror':
				tcpClisSock.send('exit')
				return 3
			elif remessage=='No':
				if num >2:
					tcpClisSock.send('exit')
					return 2
				else:
					
					while True:
						print 'name or password is error , 1 : input again  0 :Go out '
						num1 = raw_input('>')
						if num1 =='1':
							if num>2:
								return 2
							else:
								break
						elif num1 =='0' :
							tcpClisSock.send('exit')
							return 2
						else:
							continue
			elif remessage=='False':
				return 2
			elif not remessage:
					print 'server is disconnect '
					tcpClisSock.close()
					sys.exit()
		else:
			num=num+1
			message = raw_input('input you name&&password:>')
			message1=''.join(message.split(' '))
			if not message1:
				print 'Do Not onely input  spacing,  please input again !!!!'
			else:
				num3 = message1.find('&&')
				leng = len(message1)
				cha = leng-num3
				if num3==0 or num3 ==-1:
					print 'input you \'name&&password\':>'
				elif cha==2:
					print 'input password or exit'
				else:
					tcpClisSock.send(message1)
					sleep(0.5)




def Register(tcpClisSock):
	print 'please input you name and password,not noly input spacing or input \'exit\' go out'
	while True:
		rlist = [sys.stdin,tcpClisSock]
		read_list,write_list,error_list=select.select(rlist,[],[],0.2)
		if tcpClisSock in read_list:
			remessage=tcpClisSock.recv(BUFSIZE)
			if remessage=='registerok':
				tcpClisSock.send('exit')
				return 1
			elif remessage=='sqlerror':
				tcpClisSock.send('exit')
				return 3
			elif not remessage:
				print 'server is disconnect '
				sys.exit()
		else:
			print 'form like   nmae&&password'
			message=raw_input('name&&password (Must not use \'exit\' as name)>>')
			if message=='exit':
				tcpClisSock.send('exit')
				return 2
			else:
				message1=''.join(message.split(' '))
				num = message1.find('&&')
				leng=len(message1)
				cha = leng-num
				if num == -1 or num ==0:
					print 'please input name  password or exit '
				elif cha==2:
					print 'input password or exit'
				else:
					spmessage=message1.split('&&',1)
					if spmessage[0]=='exit':
						print 'must not use \'exit\' as name'
					else:
						tcpClisSock.send(message1)
						sleep(0.5)




def chatFriend(tcpClisSock):
	print 'please input you friend name and you message  like \' friendname::message\''
	while True:
		rlist = [sys.stdin,tcpClisSock]
		read_list,write_list,error_list=select.select(rlist,[],[],0.2)
		if tcpClisSock in read_list:
			remessage = tcpClisSock.recv(BUFSIZE)
			print remessage
			if remessage=='None':
				print 'you have no friend'
				return 2
			elif remessage=='youfriendisnotonline':
				print 'you friend is not on line'
				continue
			elif remessage=='thisnotisyoufriend':
				print 'he not is your friend'
				continue
			else:
				print   '                                                                                                                         '+remessage

		else:
			message=raw_input('fname::message>>')
			if message=='exit':
				tcpClisSock.send('exit')
				print 'you leave from chatroom'
				return 1
			else:
				num=message.find('::')
				if num==-1 or num==0:
					print'please input you friend name'
				else:
					tcpClisSock.send(message)
					sleep(0.5)






def andfriend(tcpClisSock):
	print 'please imput your friend name:'
	while True:
		rlist = [sys.stdin,tcpClisSock]
		read_list,write_list,error_list=select.select(rlist,[],[],0.2)
		if tcpClisSock in read_list:
			remessage=tcpClisSock.recv(BUFSIZE)
			if remessage=='noone':
				print 'dont not have this user,you can input again and \' exit\' go out'
			elif remessage=='sqlerror':
				tcpClisSock.send('exit')
				return 3
			elif remessage=='addok':
				tcpClisSock.send('exit')
				return 1
			elif not remessage:
				print 'server is disconnect '
				sys.exit()
			elif remessage=='isyou':
				print 'you can not and youself'
		else:
                                	message = raw_input('your friend name:')
                                	if not message=='exit':
                                		message1=''.join(message.split(' '))
                                		tcpClisSock.send(message1)
                                		sleep(0.5)
                                	else:
                                		tcpClisSock.send('exit')
                                		return 2


def deletefriend(tcpClisSock):
	print 'please input you friend name'
	while True:
		rlist = [sys.stdin,tcpClisSock]
		read_list,write_list,error_list=select.select(rlist,[],[],0.2)
		if tcpClisSock in read_list:
			remessage=tcpClisSock.recv(BUFSIZE)
			if remessage=='sqlerror':
				tcpClisSock.send('exit')
				return 3
			elif  remessage=='deleteok':
				tcpClisSock.send('exit')
				return 1
			elif remessage=='nofriend':
				print 'you dont have this friend you can again and get out'

			elif not remessage:
				print 'server is disconnect '
				sys.exit()
			elif remessage=='isyou':
				print'you can not delete youself'
		else:
			message=raw_input('friend name or \'exit\'>')
			message1=''.join(message.split(' '))
			if message1:
				if  not message1=='exit':
					tcpClisSock.send(message1)
					sleep(0.5)
				else:
					tcpClisSock.send('exit')
					return 2
			else:
				print 'name is spaceing'
