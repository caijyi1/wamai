'''
Created by auto_sdk on 2013.08.27
'''
from aliyun.api.base import RestApi
class Slb20130221DeleteLoadBalancerListenerRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.listenerPort = None
		self.loadBalancerId = None

	def getapiname(self):
		return 'slb.aliyuncs.com.DeleteLoadBalancerListener.2013-02-21'
