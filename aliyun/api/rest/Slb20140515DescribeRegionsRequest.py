'''
Created by auto_sdk on 2015.05.28
'''
from aliyun.api.base import RestApi
class Slb20140515DescribeRegionsRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'slb.aliyuncs.com.DescribeRegions.2014-05-15'
