'''
Created by auto_sdk on 2015.10.10
'''
from aliyun.api.base import RestApi
class Ecs20130110ResetDiskRequest(RestApi):
	def __init__(self,domain='ecs.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DiskId = None
		self.InstanceId = None
		self.SnapshotId = None

	def getapiname(self):
		return 'ecs.aliyuncs.com.ResetDisk.2013-01-10'
