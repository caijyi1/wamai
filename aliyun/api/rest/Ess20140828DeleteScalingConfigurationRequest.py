'''
Created by auto_sdk on 2014.10.14
'''
from aliyun.api.base import RestApi
class Ess20140828DeleteScalingConfigurationRequest(RestApi):
	def __init__(self,domain='ess.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ScalingConfigurationId = None

	def getapiname(self):
		return 'ess.aliyuncs.com.DeleteScalingConfiguration.2014-08-28'
