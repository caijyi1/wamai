'''
Created by auto_sdk on 2013.07.30
'''
from aliyun.api.base import RestApi
class Ocs20130801DescribeOcsMonitorRequest(RestApi):
	def __init__(self,domain='ocs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.MonitorKey = None
		self.OcsInstanceId = None

	def getapiname(self):
		return 'ocs.aliyuncs.com.DescribeOcsMonitor.2013-08-01'
