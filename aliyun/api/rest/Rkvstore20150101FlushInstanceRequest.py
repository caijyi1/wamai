'''
Created by auto_sdk on 2015.02.26
'''
from aliyun.api.base import RestApi
class Rkvstore20150101FlushInstanceRequest(RestApi):
	def __init__(self,domain='r-kvstore.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.InstanceId = None

	def getapiname(self):
		return 'r-kvstore.aliyuncs.com.FlushInstance.2015-01-01'
