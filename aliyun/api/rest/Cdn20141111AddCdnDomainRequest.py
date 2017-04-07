'''
Created by auto_sdk on 2015.06.29
'''
from aliyun.api.base import RestApi
class Cdn20141111AddCdnDomainRequest(RestApi):
	def __init__(self,domain='cdn.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.CdnType = None
		self.DomainName = None
		self.SourceType = None
		self.Sources = None
		self.SslFlag = None

	def getapiname(self):
		return 'cdn.aliyuncs.com.AddCdnDomain.2014-11-11'
