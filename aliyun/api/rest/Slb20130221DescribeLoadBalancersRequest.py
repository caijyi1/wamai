'''
Created by auto_sdk on 2014.11.15
'''
from aliyun.api.base import RestApi
class Slb20130221DescribeLoadBalancersRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.regionId = None
		self.serverId = None

	def getapiname(self):
		return 'slb.aliyuncs.com.DescribeLoadBalancers.2013-02-21'
