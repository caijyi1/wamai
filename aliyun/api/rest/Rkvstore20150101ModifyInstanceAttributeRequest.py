'''
Created by auto_sdk on 2015.02.26
'''
from aliyun.api.base import RestApi
class Rkvstore20150101ModifyInstanceAttributeRequest(RestApi):
	def __init__(self,domain='r-kvstore.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.InstanceId = None
		self.InstanceName = None
		self.NewPassword = None

	def getapiname(self):
		return 'r-kvstore.aliyuncs.com.ModifyInstanceAttribute.2015-01-01'
