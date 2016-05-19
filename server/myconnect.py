#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
class MyConnectDb(object):
	def __init__(self,connect = 'mysql+mysqldb://root:102112@localhost/Myqq'):
		self.DB_connect = connect
		self.engine = create_engine(self.DB_connect , echo=False)
		self.DB_Session = sessionmaker(bind=self.engine)
	def getSession(self):
		return self.DB_Session

