'''
Created by auto_sdk on 2015.02.10
'''
from aliyun.api.base import RestApi
class Ecs20140526ModifyEipAddressAttributeRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.AllocationId = None
		self.Bandwidth = None

	def getapiname(self):
		return 'ecs.aliyuncs.com.ModifyEipAddressAttribute.2014-05-26'
