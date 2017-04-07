'''
Created by auto_sdk on 2015.06.29
'''
from aliyun.api.base import RestApi
class Cdn20141111StopCdnDomainRequest(RestApi):
	def __init__(self,domain='cdn.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DomainName = None

	def getapiname(self):
		return 'cdn.aliyuncs.com.StopCdnDomain.2014-11-11'
