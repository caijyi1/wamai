'''
Created by auto_sdk on 2015.03.24
'''
from aliyun.api.base import RestApi
class Ecs20140526ModifyInstanceVncPasswdRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.InstanceId = None
		self.RegionId = None
		self.VncPassword = None

	def getapiname(self):
		return 'ecs.aliyuncs.com.ModifyInstanceVncPasswd.2014-05-26'
