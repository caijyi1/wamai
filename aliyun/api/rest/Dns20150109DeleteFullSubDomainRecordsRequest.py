'''
Created by auto_sdk on 2015.09.18
'''
from aliyun.api.base import RestApi
class Dns20150109DeleteFullSubDomainRecordsRequest(RestApi):
	def __init__(self,domain='dns.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.SubDomain = None
		self.Type = None

	def getapiname(self):
		return 'dns.aliyuncs.com.DeleteFullSubDomainRecords.2015-01-09'
