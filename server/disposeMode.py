#!/usr/bin/env python
from operateDb import *
from mymd5 import *
import types
BUFSIZE=1024
def ServerLogic(TcpScoket,DB_Session,mutex,Online):

	operateDb = OperateDb(DB_Session)
	myOnlineFriend={}
	myFriend={}
	myid=0
	myOnline={}
	myname=' '
	flge = 0
	while  True:
		message = TcpScoket.recv(BUFSIZE)
		print message
		if message=='1':
			if flge == 1:
				TcpScoket.send('you had long in')
			else:
				re= Longin(TcpScoket,operateDb)
				if re !=' ':
					row = re.rowcount
					if row>0:
						flge=1
						for rre in re.fetchall():
							myname = rre['uname']
							myid=rre['id']
						setDiction(myname,TcpScoket,mutex,Online)
						if mutex.acquire(1): 
							myOnline=getDiction(Online)
							mutex.release()
						getFriend(operateDb,myid,myOnlineFriend,myFriend,myOnline)
				else:
					continue

		elif message=='2':
			register(TcpScoket,operateDb)
			
		elif message=='3' and flge==1:
			chatRoom(TcpScoket,operateDb,myid,myname,myOnlineFriend,myFriend,myOnline)
		elif message=='4' and flge==1:
			print '44444'
			addFriend(TcpScoket,operateDb,myid,myname)
		elif message=='5' and flge==1:
			deleteFriend(TcpScoket,operateDb,myOnlineFriend,myFriend,myid,myname)
		elif message=='6'and flge==1:
			creadeTribe(TcpScoket,operateDb)
		elif message=='7' and flge==1:
			tribeChat(TcpScoket,operateDb)
		elif message=='exit':
			operateDb.sessionClose()
			TcpScoket.close()
			break



def setDiction(uname,TcpScoket,mutex,Online):
	if mutex.acquire(1): 
		Online.setdefault(uname,TcpScoket)
		mutex.release()




def getDiction(Online):
	return Online

def getFriend(operateDb,myid,myOnlineFriend,myFriend,myOnline):
	select_dic = {'myid':myid}
	sql =text('select * from user ,friend  where  friend.uid =:myid  and friend.fid = user.id ')
	re = operateDb.operateDb(sql,select_dic)
	if re != 0 and re !=1:
		row = re.rowcount
		if row>0:
			for ree in re.fetchall():
				myFriend.setdefault(ree['uname'],ree['fid']) 
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
			spmessage=message.split('::',1)
			friendname=spmessage[0]
			if not myFriend.has_key(friendname):
				mes = 'thisnotisyoufriend'
				TcpScoket.send(mes)
				continue
			elif not myOnlineFriend.has_key(friendname):
				TcpScoket.send('youfriendisnotonline')
				continue
			else:
				sendmessage = spmessage[1]+"::"+myname
				myOnlineFriend[friendname].send(sendmessage)
		
		else:
			break





def addFriend(TcpScoket,operateDb,myid,myname):
	while  True:
		message = TcpScoket.recv(BUFSIZE)
		if message==myname:
			TcpScoket.send('isyou')
			continue
		if not message=='exit':
			select_dic={'name':message}
			sql =text( 'select * from user where uname= :name')
			re = operateDb.operateDb(sql,select_dic)
			if re != 0 and re !=1:
				row =  re.rowcount
				if row==0:
					TcpScoket.send('noone')
					
				else:
					for ress in  re.fetchall():
						fid = ress['id']
					insert_dic={'myid':myid,'fid':fid}
					sql=text('insert into friend(uid,fid) values (:myid,:fid)')
					re = operateDb.operateDb(sql,insert_dic)
					if re !=0 and re !=1:
						TcpScoket.send('addok')
			else:
				TcpScoket.send('sqlerror')
		else:
			break



def deleteFriend(TcpScoket,operateDb,myOnlineFriend,myFriend,myid,myname):
	while True:
		message = TcpScoket.recv(BUFSIZE)
		if message==myname:
			TcpScoket.send('isyou')
			continue
		if not message=='exit':
			if myFriend.has_key(message):
				fid = myFriend[message]
				del myFriend[message]
			else:
				TcpScoket.send('nofriend')
				continue

			if myOnlineFriend.has_key(message):
				del myOnlineFriend[message]
			delete_dic={'myid':myid,'fid':fid}
			sql = text('delete from friend where uid = :myid and fid = :fid')
			re = operateDb.operateDb(sql,delete_dic)
			if re != 0 and re !=1:
				if re.rowcount>0:
					TcpScoket.send('deleteok')
				else:
					TcpScoket.send('nofriend')
				
			else:
				TcpScoket.send('sqlerror')
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
			spmessage=message.split('&&',1)
			myuname=spmessage[0]
			mypassword = spmessage[1]
			if type(mypassword)  is not  types.StringType:
				try:
					mypassword = str(mypassword)
				except TypeError:
					TcpScoket.send('sqlerror')


			mypassword=Mymd5(mypassword)
			select_dic={'name':myuname,'password':mypassword}
			sql = 'select *from user  where uname=:name and password= :password'
			re = operateDb.operateDb(sql,select_dic)
			if re ==0 or re==1:
				TcpScoket.send('sqlerror')
			else:
				row = re.rowcount
				if row >0:
					TcpScoket.send('Loginok')
					return re
				else :
					TcpScoket.send('No')
		else:
			return ' '
	if fge >=2:
		TcpScoket.send('False')
		return ' '
		







def register(TcpScoket,operateDb):
	while True:
		message= TcpScoket.recv(BUFSIZE);
		if not message=='exit':
			spmessage = message.split('&&',1)
			myuname = spmessage[0]
			mypassword = spmessage[1]
			if type(mypassword) is not types.StringType:
				try:
					mypassword = str(mypassword)
				except TypeError:
					TcpScoket.send('sqlerror')
			mypassword = Mymd5(mypassword)
			insert_dic={'myuname':myuname,'mypassword':mypassword}
                                                 
			sql = 'insert into user (uname,password) values (:myuname,:mypassword)'
			re=operateDb.operateDb(sql,insert_dic)
			if re ==0 or re == 1:
				TcpScoket.send('sqlerror')
			else:
				TcpScoket.send('registerok')
		else:
			return