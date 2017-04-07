'''
Created by auto_sdk on 2015.08.06
'''
from aliyun.api.base import RestApi
class Dns20150109DeleteSubDomainRecordsRequest(RestApi):
	def __init__(self,domain='dns.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.domainName = None
		self.rr = None
		self.type = None

	def getapiname(self):
		return 'dns.aliyuncs.com.DeleteSubDomainRecords.2015-01-09'
