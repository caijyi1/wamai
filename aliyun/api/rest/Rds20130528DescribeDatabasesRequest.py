'''
Created by auto_sdk on 2015.04.27
'''
from aliyun.api.base import RestApi
class Rds20130528DescribeDatabasesRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.DBName = None
		self.DBStatus = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribeDatabases.2013-05-28'
