'''
Created by auto_sdk on 2014.11.15
'''
from aliyun.api.base import RestApi
class Slb20130221SetLoadBalancerTCPListenerAttributeRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.HealthyThreshold = None
		self.UnhealthyThreshold = None
		self.connectPort = None
		self.connectTimeout = None
		self.healthCheck = None
		self.interval = None
		self.listenerPort = None
		self.loadBalancerId = None
		self.persistenceTimeout = None
		self.scheduler = None

	def getapiname(self):
		return 'slb.aliyuncs.com.SetLoadBalancerTCPListenerAttribute.2013-02-21'
