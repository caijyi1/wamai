'''
Created by auto_sdk on 2013.08.28
'''
from aliyun.api.base import RestApi
class Slb20130221DescribeBackendServersRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.listenerPort = None
		self.loadBalancerId = None

	def getapiname(self):
		return 'slb.aliyuncs.com.DescribeBackendServers.2013-02-21'
