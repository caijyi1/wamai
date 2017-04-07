'''
Created by auto_sdk on 2015.08.06
'''
from aliyun.api.base import RestApi
class Dns20150109DescribeSubDomainRecordsRequest(RestApi):
	def __init__(self,domain='dns.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.PageNumber = None
		self.PageSize = None
		self.SubDomain = None
		self.Type = None

	def getapiname(self):
		return 'dns.aliyuncs.com.DescribeSubDomainRecords.2015-01-09'
