'''
Created by auto_sdk on 2015.09.25
'''
from aliyun.api.base import RestApi
class Rds20140815DescribeDBInstancePerformanceRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.EndTime = None
		self.Key = None
		self.StartTime = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribeDBInstancePerformance.2014-08-15'
