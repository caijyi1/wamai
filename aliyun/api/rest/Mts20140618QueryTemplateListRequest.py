'''
Created by auto_sdk on 2015.09.01
'''
from aliyun.api.base import RestApi
class Mts20140618QueryTemplateListRequest(RestApi):
	def __init__(self,domain='mts.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.TemplateIds = None

	def getapiname(self):
		return 'mts.aliyuncs.com.QueryTemplateList.2014-06-18'
