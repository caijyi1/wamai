'''
Created by auto_sdk on 2015.10.09
'''
from aliyun.api.base import RestApi
class Ecs20130110DescribeInstanceAttributeRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.InstanceId = None

	def getapiname(self):
		return 'ecs.aliyuncs.com.DescribeInstanceAttribute.2013-01-10'
