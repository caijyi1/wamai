'''
Created by auto_sdk on 2015.01.08
'''
from aliyun.api.base import RestApi
class Rds20140815ModifyBackupPolicyRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.PreferredBackupPeriod = None
		self.PreferredBackupTime = None

	def getapiname(self):
		return 'rds.aliyuncs.com.ModifyBackupPolicy.2014-08-15'
