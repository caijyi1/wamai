'''
Created by auto_sdk on 2014.11.17
'''
from aliyun.api.base import RestApi
class Ecs20140526DetachDiskRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DiskId = None
		self.InstanceId = None

	def getapiname(self):
		return 'ecs.aliyuncs.com.DetachDisk.2014-05-26'
