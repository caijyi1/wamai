'''
Created by auto_sdk on 2015.09.22
'''
from aliyun.api.base import RestApi
class Mts20140618QuerySnapshotJobListRequest(RestApi):
	def __init__(self,domain='mts.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.SnapshotJobIds = None

	def getapiname(self):
		return 'mts.aliyuncs.com.QuerySnapshotJobList.2014-06-18'
