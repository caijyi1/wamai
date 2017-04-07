'''
Created by auto_sdk on 2015.08.25
'''
from aliyun.api.base import RestApi
class Rds20140815SwitchDBInstanceHARequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DbInstanceId = None
		self.Force = None
		self.NodeId = None
		self.Operation = None

	def getapiname(self):
		return 'rds.aliyuncs.com.SwitchDBInstanceHA.2014-08-15'
