'''
Created by auto_sdk on 2015.02.03
'''
from aliyun.api.base import RestApi
class Rds20140815DescribeSQLLogReportsRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.EndTime = None
		self.PageNumber = None
		self.PageSize = None
		self.ReportType = None
		self.StartTime = None

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribeSQLLogReports.2014-08-15'
