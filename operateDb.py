#!/usr/bin/env python
from sqlalchemy import *
class OperateDb(object):
	def __init__(self,DB_Session):
		self.DB_Session=DB_Session
		self.session = self.DB_Session()

	def selectDB(self,sql):
		query = self.session.execute(sql)
		return query

	def insertDB(self,sql):
		query = self.session.execute(sql)
		return query

	def deleteDB(self,sql):
		query = self.session.execute(sql)
		return query
	def updateDB(self,sql):
		query = self.session.execute(sql)
		return query
	def sessionClose(self):
		self.session.close()
	def operateDb(self,sql):
		try:
			query = self.session.execute(sql)
			self.session.commit()
		except sqlalchemy.exc.OperationalError:
			query = 0
		except sqlalchemy.exc.IntegrityError:
			query = 1
		finally:
			return query