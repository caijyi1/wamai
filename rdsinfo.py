#!/usr/bin/env python
#-*- coding:utf-8 -*-
#__author__ = 'jony'

import aliyun.api
import sys
from optparse import OptionParser
import argparse
import pprint

class App_aliyun():

    def __init__(self):
        self.rdsinfo = {}
        self.access_key_id = 'hTz6eVASJGn8T9Jd'
        self.access_key_secret = 'ynI2TjILICcA3L1gAouOVRNfM9xyMk'
        aliyun.setDefaultAppInfo(self.access_key_id,self.access_key_secret)

    def getdbins(self,project): 
        ddr = aliyun.api.Rds20130528DescribeDBInstancesRequest()
        sponse = ddr.getResponse()
        if "Code" in  sponse:
            print "获取结果有误,请确认传入参数正确！"
            sys.exit(1)
        rdslist = []
        for i in sponse['Items']['DBInstance']:
            if project in i['DBInstanceDescription']:
                rdslist.append(i['DBInstanceId'])
        return rdslist

    def getdatabase(self,*rdsid):
        rddr=aliyun.api.Rds20140815DescribeDatabasesRequest()
        for _id in rdsid:
            dblist = []
            rddr.DBInstanceId = _id
            rddr.getApplicationParameters()
            sponse = rddr.getResponse()
            if "Code" in sponse:
                print "获取结果出错,请确认传入参数！"
                sys.exit(1)
            for i in sponse['Databases']['Database']:
                if 'configdb' in i['DBName']:
                    dblist.append(i['DBName'])
            self.rdsinfo[_id] = len(dblist)
        return self.rdsinfo

    def grantprivige(self,rdsid,dbname,dbuser,privilege='ReadWrite'):
        '''privilege:[ReadWrite|ReadOnly]'''
        rgapr = aliyun.api.Rds20140815GrantAccountPrivilegeRequest()
        rgapr.DBInstanceId = rdsid
        rgapr.DBName = dbname
        rgapr.AccountName = dbuser 
        rgapr.AccountPrivilege = privilege
        sponse = rgapr.getResponse()
        if "Code" in sponse:
            print "获取结果出错,请确认传入参数！错误代码: %s" % sponse['Code']
            sys.exit(1)
        print "数据库%s授权%s%s成功!" %(dbname,dbuser,privilege)

    def getfreerds(self,project):
        rdsids = self.getdbins(project)
        rdsfree = self.getdatabase(*rdsids)
        return min(rdsfree.items(),key=lambda x:x[1])[0]


def main():
	parser = argparse.ArgumentParser(description="Get the moust free Rds.",usage="Prog [options]")
	parser.add_argument("-p",'--project', default='warfare',help='Game project! Example:[warfare|warfare_ly|airfight]')
	parser.add_argument("-v","--verbose",action="store_true",help="Print Version")
	args = parser.parse_args()
	if args.verbose:
		print "1.0"
	if args.project in ['warfare','warfare_ly','airfight']:
		print App_aliyun().getfreerds(args.project)
	else:
		print "阿里云上没有 %s 项目的Rds!" % args.project
	
if __name__ == '__main__':
	main()
    
    
    
