'''
Created by auto_sdk on 2015.01.22
'''
from aliyun.api.base import RestApi
class Rds20140815ImportDataFromDatabaseRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.ImportDataType = None
		self.IsLockTable = None
		self.SourceDatabaseDBNames = None
		self.SourceDatabaseIp = None
		self.SourceDatabasePassword = None
		self.SourceDatabasePort = None
		self.SourceDatabaseUserName = None

	def getapiname(self):
		return 'rds.aliyuncs.com.ImportDataFromDatabase.2014-08-15'
