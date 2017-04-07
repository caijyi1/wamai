'''
Created by auto_sdk on 2015.08.04
'''
from aliyun.api.base import RestApi
class Rds20140815CreateAccountRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.AccountDescription = None
		self.AccountName = None
		self.AccountPassword = None
		self.DBInstanceId = None
		self.resourceOwnerAccount = None
		self.resourceOwnerId = None

	def getapiname(self):
		return 'rds.aliyuncs.com.CreateAccount.2014-08-15'
