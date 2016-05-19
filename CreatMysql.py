#!/usr/bin/env python
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import  *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import sqlalchemy

DB_CONNECT = 'mysql+mysqldb://root:102112@localhost/Myqq'
engine = create_engine(DB_CONNECT, echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
'''
dic = {'id':1}
sql = text("select * from user ,friend  where  friend.uid = :id and friend.fid = user.id")
quer = session.execute(sql,dic)
if   not quer :
	print 'none'
print quer.rowcount
for re in quer.fetchall():
           
	print re['id'],re['uname'],re['password'];
	print re.id,re['uname'],re['password'];
'''
insert_dic={'uid':1,'fid':2}
sql = text('delete from friend where uid=:uid and fid=:fid')
query=session.execute(sql,insert_dic)
print query.rowcount


session.commit()
session.close()

