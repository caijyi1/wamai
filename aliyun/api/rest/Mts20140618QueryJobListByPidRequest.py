'''
Created by auto_sdk on 2015.07.30
'''
from aliyun.api.base import RestApi
class Mts20140618QueryJobListByPidRequest(RestApi):
	def __init__(self,domain='mts.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.PageNumber = None
		self.PageSize = None
		self.PipelineId = None

	def getapiname(self):
		return 'mts.aliyuncs.com.QueryJobListByPid.2014-06-18'
