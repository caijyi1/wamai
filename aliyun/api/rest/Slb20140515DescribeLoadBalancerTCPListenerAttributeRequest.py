'''
Created by auto_sdk on 2015.07.17
'''
from aliyun.api.base import RestApi
class Slb20140515DescribeLoadBalancerTCPListenerAttributeRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ListenerPort = None
		self.LoadBalancerId = None

	def getapiname(self):
		return 'slb.aliyuncs.com.DescribeLoadBalancerTCPListenerAttribute.2014-05-15'
