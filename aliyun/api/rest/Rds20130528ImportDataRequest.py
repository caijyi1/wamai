'''
Created by auto_sdk on 2014.10.21
'''
from aliyun.api.base import RestApi
class Rds20130528ImportDataRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.FileName = None

	def getapiname(self):
		return 'rds.aliyuncs.com.ImportData.2013-05-28'
