#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
class ConnectDb(object):
	def  __init__(self,connect = 'mysql+mysqldb://root:102112@localhost/Myqq'):
		self.DB_CONNECT1=connect
		print self.DB_CONNECT1

	def run(self):
		global engine = create_engine(self.DB_CONNECT1, echo=False)
		global DB_Session = sessionmaker(bind=engine)

	def getSession(self):
		return global DB_Session

