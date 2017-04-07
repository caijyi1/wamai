'''
Created by auto_sdk on 2014.10.14
'''
from aliyun.api.base import RestApi
class Rds20130528CreateAccountRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.AccountDescription = None
		self.AccountName = None
		self.AccountPassword = None
		self.AccountPrivilege = None
		self.DBInstanceId = None
		self.DBName = None

	def getapiname(self):
		return 'rds.aliyuncs.com.CreateAccount.2013-05-28'
