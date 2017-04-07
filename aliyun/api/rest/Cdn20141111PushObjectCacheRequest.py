'''
Created by auto_sdk on 2015.07.10
'''
from aliyun.api.base import RestApi
class Cdn20141111PushObjectCacheRequest(RestApi):
	def __init__(self,domain='cdn.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ObjectPath = None

	def getapiname(self):
		return 'cdn.aliyuncs.com.PushObjectCache.2014-11-11'
