'''
Created by auto_sdk on 2015.08.06
'''
from aliyun.api.base import RestApi
class Rds20140815ModifyParameterRequest(RestApi):
	def __init__(self,domain='rds.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.DBInstanceId = None
		self.Forcerestart = None
		self.Parameters = None

	def getapiname(self):
		return 'rds.aliyuncs.com.ModifyParameter.2014-08-15'
