'''
Created by auto_sdk on 2015.08.13
'''
from aliyun.api.base import RestApi
class Rds20140815DescribeDBInstanceHAConfigRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DbInstanceId = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribeDBInstanceHAConfig.2014-08-15'
