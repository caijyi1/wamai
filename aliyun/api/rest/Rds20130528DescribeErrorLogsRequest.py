'''
Created by auto_sdk on 2014.10.14
'''
from aliyun.api.base import RestApi
class Rds20130528DescribeErrorLogsRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.EndTime = None
		self.PageNumber = None
		self.PageSize = None
		self.StartTime = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribeErrorLogs.2013-05-28'
