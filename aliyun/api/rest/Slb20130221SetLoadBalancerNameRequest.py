'''
Created by auto_sdk on 2013.09.02
'''
from aliyun.api.base import RestApi
class Slb20130221SetLoadBalancerNameRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.loadBalancerId = None
		self.loadBalancerName = None

	def getapiname(self):
		return 'slb.aliyuncs.com.SetLoadBalancerName.2013-02-21'
