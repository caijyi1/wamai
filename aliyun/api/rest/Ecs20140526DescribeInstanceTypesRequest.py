'''
Created by auto_sdk on 2014.07.23
'''
from aliyun.api.base import RestApi
class Ecs20140526DescribeInstanceTypesRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'ecs.aliyuncs.com.DescribeInstanceTypes.2014-05-26'
