'''
Created by auto_sdk on 2015.09.01
'''
from aliyun.api.base import RestApi
class Mts20140618SearchTemplateRequest(RestApi):
	def __init__(self,domain='mts.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.PageNumber = None
		self.PageSize = None
		self.State = None

	def getapiname(self):
		return 'mts.aliyuncs.com.SearchTemplate.2014-06-18'
