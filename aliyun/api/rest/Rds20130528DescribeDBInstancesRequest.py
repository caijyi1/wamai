'''
Created by auto_sdk on 2014.11.17
'''
from aliyun.api.base import RestApi
class Rds20130528DescribeDBInstancesRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.DBInstanceNetType = None
		self.DBInstanceStatus = None
		self.Engine = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribeDBInstances.2013-05-28'
