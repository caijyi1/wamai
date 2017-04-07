'''
Created by auto_sdk on 2015.01.22
'''
from aliyun.api.base import RestApi
class Rds20140815DescribePreCheckResultsRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.PreCheckId = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribePreCheckResults.2014-08-15'
