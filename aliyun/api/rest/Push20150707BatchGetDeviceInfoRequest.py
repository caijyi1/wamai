'''
Created by auto_sdk on 2015.07.08
'''
from aliyun.api.base import RestApi
class Push20150707BatchGetDeviceInfoRequest(RestApi):
	def __init__(self,domain='push.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.Appid = None
		self.Devices = None

	def getapiname(self):
		return 'push.aliyuncs.com.batchGetDeviceInfo.2015-07-07'
