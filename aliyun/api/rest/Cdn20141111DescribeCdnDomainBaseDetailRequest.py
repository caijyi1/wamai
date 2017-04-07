'''
Created by auto_sdk on 2015.08.10
'''
from aliyun.api.base import RestApi
class Cdn20141111DescribeCdnDomainBaseDetailRequest(RestApi):
	def __init__(self,domain='cdn.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DomainName = None

	def getapiname(self):
		return 'cdn.aliyuncs.com.DescribeCdnDomainBaseDetail.2014-11-11'
