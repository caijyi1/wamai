'''
Created by auto_sdk on 2015.08.04
'''
from aliyun.api.base import RestApi
class Rds20140815DeleteDatabaseRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.DBName = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DeleteDatabase.2014-08-15'
