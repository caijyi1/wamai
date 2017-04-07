'''
Created by auto_sdk on 2015.03.25
'''
from aliyun.api.base import RestApi
class Rds20140815ModifyDBInstanceConnectionStringRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ConnectionStringPrefix = None
		self.CurrentConnectionString = None
		self.DBInstanceId = None
		self.Port = None

	def getapiname(self):
		return 'rds.aliyuncs.com.ModifyDBInstanceConnectionString.2014-08-15'
