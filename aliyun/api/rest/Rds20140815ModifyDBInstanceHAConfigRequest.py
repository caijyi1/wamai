'''
Created by auto_sdk on 2015.08.25
'''
from aliyun.api.base import RestApi
class Rds20140815ModifyDBInstanceHAConfigRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DbInstanceId = None
		self.HAMode = None
		self.SyncMode = None

	def getapiname(self):
		return 'rds.aliyuncs.com.ModifyDBInstanceHAConfig.2014-08-15'
