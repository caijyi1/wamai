'''
Created by auto_sdk on 2015.09.24
'''
from aliyun.api.base import RestApi
class Rds20140815DescribeAccountsRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.AccountName = None
		self.DBInstanceId = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribeAccounts.2014-08-15'
