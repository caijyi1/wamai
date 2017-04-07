'''
Created by auto_sdk on 2015.09.22
'''
from aliyun.api.base import RestApi
class Mts20140618AddPipelineRequest(RestApi):
	def __init__(self,domain='mts.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.Name = None
		self.NotifyConfig = None
		self.Role = None
		self.Speed = None

	def getapiname(self):
		return 'mts.aliyuncs.com.AddPipeline.2014-06-18'
