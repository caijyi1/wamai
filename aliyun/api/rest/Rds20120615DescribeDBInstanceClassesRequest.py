'''
Created by auto_sdk on 2013.12.27
'''
from aliyun.api.base import RestApi
class Rds20120615DescribeDBInstanceClassesRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'rds.aliyuncs.com.DescribeDBInstanceClasses.2012-06-15'
