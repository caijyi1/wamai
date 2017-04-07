'''
Created by auto_sdk on 2015.07.08
'''
from aliyun.api.base import RestApi
class Push20150707BatchRegisteRequest(RestApi):
	def __init__(self,domain='push.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.Appid = None
		self.Limit = None

	def getapiname(self):
		return 'push.aliyuncs.com.batchRegiste.201507-07'
