'''
Created by auto_sdk on 2015.07.17
'''
from aliyun.api.base import RestApi
class Slb20140515DescribeLoadBalancerAttributeRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.LoadBalancerId = None

	def getapiname(self):
		return 'slb.aliyuncs.com.DescribeLoadBalancerAttribute.2014-05-15'
