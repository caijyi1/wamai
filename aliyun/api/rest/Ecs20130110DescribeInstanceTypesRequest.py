'''
Created by auto_sdk on 2014.09.28
'''
from aliyun.api.base import RestApi
class Ecs20130110DescribeInstanceTypesRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'ecs.aliyuncs.com.DescribeInstanceTypes.2013-01-10'
