#!/usr/bin/env python
from operateDb import *
BUFSIZE=1024
def ServerLogic(TcpScoket,DB_Session):

	operateDb = OperateDb(DB_Session)
	myOnlineFriend={}
	myFriend={}
	myid=0
	myOnline={}
	myname=' '
	flge = 0
	while  True:
		message = TcpScoket.recv(BUFSIZE)
		if message==1:
			if flge == 1:
				TcpScoket.send('you had long in')
			else:
				re= Longin(TcpScoket,operateDb)
				row = re.rowcount
				if row>0:
					flge=1
				for rre in re.fetchall():
					myname = rre['uname']
					myid=rre['id']
				setDiction(myname,TcpScoket)
				if mutex.acquire(1): 
					myOnline=getDiction()
					mutex.release()
				
				getFriend(operateDb,myid,myOnlineFriend,myFriend,myOnline)


			
			
		elif message==2:
			register(TcpScoket,operateDb)
			
		elif message==3 and flge==1:
			chatRoom(TcpScoket,operateDb,myid,myname,myOnlineFriend,myFriend,myOnline)
			
		elif message==4 and flge==1:
			addFriend(TcpScoket,operateDb,myid)
		elif message==5 and flge==1:
			deleteFriend(TcpScoket,operateDb,myOnlineFriend,myFriend,myid)
		elif message==6 and flge==1:
			creadeTribe(TcpScoket,operateDb)
		elif message==7 and flge==1:
			tribeChat(TcpScoket,operateDb)
		elif message=='exit':
			operateDb.sessionClose()
			TcpScoket.close()
			break



def setDiction(uname,TcpScoket):
	if mutex.acquire(1): 
		Online.setdefault(uname,TcpScoket)
		mutex.release()




def getDiction():
	return Online

def getFriend(operateDb,myid,myOnlineFriend,myFriend,myOnline):
	sql ='select * from user ,friend  where  friend.uid =myid and friend.fid = user.id '
	re = operateDb.operateDb(sql)
	if re != 0 and re !=1:
		row = re.rowcount
		if row>0:
			for ree in re.fetchall():
				myFriend.setdefault(ree[uname],ree['fid']) 
				if myOnline.has_key(ree['uname']):
					myOnlineFriend.setdefault(ree['uname'],myOnline[ree['uname']])

def chatRoom(TcpScoket,operateDb,myid,myname,myOnlineFriend,myFriend,myOnline):
	getFriend(operateDb,myid,myOnlineFriend,myFriend,myOnline)
	if len(myFriend)==0:
		TcpScoket.send('None')
		
		return	
	while True:
		message = TcpScoket.recv(BUFSIZE)
		if  not message == 'exit':
			spmessage=message.spilt('::')
			friendname=spmessage[0]
			if not myFriend.has_key(friendname):
				mes = friendname+',is not you  friend ,you can find  out he'
				TcpScoket.send(mes)
				continue
			elif not myOnlineFriend.has_key(friendname):
				TcpScoket.send('you friend is not on line')
				continue
			else:
				myOnlineFriend[friendname].send(message)
		else:
			TcpScoket.send('bey')
			break


			


def addFriend(TcpScoket,operateDb,myid):
	while  True:
		message = TcpScoket.recv(BUFSIZE)
		if not message=='exit':
			sql = 'select * from user where uname=message'
			re = operateDb.operateDb(sql)
			if re != 0 and re !=1:
				row =  re.rowcount
				if row==0:
					TcpScoket.send('no one')
					
				else:
					for ress in  re.fetchall():
						fid = ress['id']
					sql='insert into friend(uid,fid) values (myid,fid)'
					re = operateDb.operateDb(sql)
					if re !=0 and re !=1:
						TcpScoket.send('add ok')
			else:
				TcpScoket.send('sql error')
		else:
			break

			
			
				
		
		

def deleteFriend(TcpScoket,operateDb,myOnlineFriend,myFriend,myid):
	while True:
		message = TcpScoket.recv(BUFSIZE)
		if not message=='exit':
			if myFriend.has_key(message):
				fid = myFriend[message]
				del myFriend[message]

			if myOnlineFriend.has_key(message):
				del myOnlineFriend[message]
			sql = 'delete from friend where uid =myid and fid = fid'
			re = operateDb.operateDb(sql)
			if re != 0 and re !=1:
				TcpScoket.send('delete ok')
			else:
				TcpScoket.send('sql error')
		else:
			break


def creadeTribe(TcpScoket,operateDb):
	pass

def tribeChat(TcpScoket,operateDb):
	pass

def Longin(TcpScoket,operateDb):
	fge = 0
	row =0
	while True and fge<3:
		fge=fge+1
		message = TcpScoket.recv(BUFSIZE)
		if  not message == 'exit':
			spmessage=message.spilt('&&')
			myuname=spmessage[0]
			mypassword = spmessage[1]
			sql = 'select *from user  where uname=myuname and password= mypassword'
			re = operateDb.operateDb(sql)
			if re ==0 or re==1:
				TcpScoket.send('sql error')
			else:
				row = re.rowcount
				if row >0:
					TcpScoket.send('Longin ok')
					return re
				else :
					TcpScoket.send('No')
		else:
			break
	if fge >=3:
		TcpScoket.send('False')
		operateDb.sessionClose()
		TcpScoket.close()
                

		



def register(TcpScoket,operateDb):
	while True:
		message= TcpScoket.recv(BUFSIZE);
		if not message=='exit':
			spmessage = message.spilt('&&')
			myuname = spmessage[0]
			mypassword = spmessage[1]
			sql = 'insert into user (uname,password) values (myuname,mypassword)'
			re=operateDb.operateDb(sql)
			if re ==0 or re == 1:
				TcpScoket.send('sql error')
			else:
				TcpScoket.send('register ok')
		else:
			return