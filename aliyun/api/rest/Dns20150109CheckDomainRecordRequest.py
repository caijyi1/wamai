'''
Created by auto_sdk on 2015.06.26
'''
from aliyun.api.base import RestApi
class Dns20150109CheckDomainRecordRequest(RestApi):
	def __init__(self,domain='dns.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DomainName = None
		self.Line = None
		self.Priority = None
		self.Rr = None
		self.RrId = None
		self.Ttl = None
		self.Type = None
		self.Value = None
		self.ViewPattern = None

	def getapiname(self):
		return 'dns.aliyuncs.com.CheckDomainRecord.2015-01-09'
