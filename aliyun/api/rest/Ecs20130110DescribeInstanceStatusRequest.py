'''
Created by auto_sdk on 2014.09.28
'''
from aliyun.api.base import RestApi
class Ecs20130110DescribeInstanceStatusRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.PageNumber = None
		self.PageSize = None
		self.RegionId = None
		self.ZoneId = None

	def getapiname(self):
		return 'ecs.aliyuncs.com.DescribeInstanceStatus.2013-01-10'
