'''
Created by auto_sdk on 2015.03.16
'''
from aliyun.api.base import RestApi
class Ecs20140526DeleteInstanceRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.InstanceId = None

	def getapiname(self):
		return 'ecs.aliyuncs.com.DeleteInstance.2014-05-26'
