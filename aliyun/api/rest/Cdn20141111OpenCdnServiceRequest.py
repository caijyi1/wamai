'''
Created by auto_sdk on 2015.05.13
'''
from aliyun.api.base import RestApi
class Cdn20141111OpenCdnServiceRequest(RestApi):
	def __init__(self,domain='cdn.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.InternetChargeType = None

	def getapiname(self):
		return 'cdn.aliyuncs.com.OpenCdnService.2014-11-11'
