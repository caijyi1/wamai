'''
Created by auto_sdk on 2015.01.23
'''
from aliyun.api.base import RestApi
class Slb20140515AddListenerWhiteListItemRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ListenerPort = None
		self.LoadBalancerId = None
		self.SourceItems = None

	def getapiname(self):
		return 'slb.aliyuncs.com.AddListenerWhiteListItem.2014-05-15'
