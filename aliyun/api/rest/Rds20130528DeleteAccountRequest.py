'''
Created by auto_sdk on 2014.10.14
'''
from aliyun.api.base import RestApi
class Rds20130528DeleteAccountRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.AccountName = None
		self.DBInstanceId = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DeleteAccount.2013-05-28'
