'''
Created by auto_sdk on 2015.10.13
'''
from aliyun.api.base import RestApi
class Rds20140815ModifySecurityIpsRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceIPArrayAttribute = None
		self.DBInstanceIPArrayName = None
		self.DBInstanceId = None
		self.SecurityIps = None

	def getapiname(self):
		return 'rds.aliyuncs.com.ModifySecurityIps.2014-08-15'
