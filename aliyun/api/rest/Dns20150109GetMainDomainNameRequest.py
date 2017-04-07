'''
Created by auto_sdk on 2015.08.17
'''
from aliyun.api.base import RestApi
class Dns20150109GetMainDomainNameRequest(RestApi):
	def __init__(self,domain='dns.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.InputString = None

	def getapiname(self):
		return 'dns.aliyuncs.com.GetMainDomainName.2015-01-09'
