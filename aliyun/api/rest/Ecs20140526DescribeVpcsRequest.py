'''
Created by auto_sdk on 2015.02.10
'''
from aliyun.api.base import RestApi
class Ecs20140526DescribeVpcsRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.PageNumber = None
		self.PageSize = None
		self.RegionId = None
		self.VpcId = None

	def getapiname(self):
		return 'ecs.aliyuncs.com.DescribeVpcs.2014-05-26'
