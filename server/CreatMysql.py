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

sql = text('select * from user ,friend  where  friend.uid =1 and friend.fid = user.id')
quer = session.execute(sql)
if   not quer :
	print 'none'
print quer.rowcount
'''for re in quer.fetchall():'''
              re =quer.first()
	print re['id'],re['uname'],re['password'];
	print re.id,re['uname'],re['password'];
'''
sql = text('insert into user(uname,password) values(null,null)')
query=session.execute(sql)
print query.rowcount

'''
session.commit()
session.close()

