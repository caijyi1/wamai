'''
Created by auto_sdk on 2015.01.27
'''
from aliyun.api.base import RestApi
class Ram20140214ListUserPoliciesRequest(RestApi):
	def __init__(self,domain='ram.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.AccountSpace = None
		self.UserName = None

	def getapiname(self):
		return 'ram.aliyuncs.com.ListUserPolicies.2014-02-14'
