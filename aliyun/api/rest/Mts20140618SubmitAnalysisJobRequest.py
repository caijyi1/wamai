'''
Created by auto_sdk on 2015.07.30
'''
from aliyun.api.base import RestApi
class Mts20140618SubmitAnalysisJobRequest(RestApi):
	def __init__(self,domain='mts.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.AnalysisConfig = None
		self.Input = None
		self.PipelineId = None
		self.Priority = None
		self.UserData = None

	def getapiname(self):
		return 'mts.aliyuncs.com.SubmitAnalysisJob.2014-06-18'
