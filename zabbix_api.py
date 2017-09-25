#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import requests
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Zabbix_Api:
    def __init__(self):
        self.url = "http://zabbix.tmsjyx.net:88/zabbix/api_jsonrpc.php"
        self.header = {"Content-Type":"application/json"}
        self.authid = self.login()

    def login(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": "Admin",
                    "password": "LPDeDW2NZKw9AES"
                },
                "id": 1
            })

        try:
            response = requests.get(self.url,data=data,headers=self.header)
            return response.json()['result']
        except:
            print "获取API接口失败,请检查url,user,password!"
            return False


    def get_alerts(self):
        ''' 获取报警'''
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "alert.get",
                "params": {
                    "output": "extend",
                    "actionids": "3"
                },
                "auth": self.authid,
                "id": 1
            })

        response = requests.get(self.url,data=data,headers=self.header)
        return json.loads(response.text)['result']

    def template_getobjects(self,*host):
        ''' 获取templateid
        host: 例如'APP_TOMCAT_CPU_MONITOR','Template ICMP Ping','Template Linux DiskIO','Server performance'
        '''
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "template.getobjects",
                "params": {
                    "host":
                    host[0],
                },
                "auth": self.authid,
                "id": 1
            })

        response = requests.get(self.url,data=data,headers=self.header)
        templateid = {}
        for result in response.json()['result']:
            templateid[result['host']]=(result['templateid'])

        return templateid

    def template_create(self,host,groups=1):
        '''host: template name
        groups: 1为template
        '''
        if host in self.template_getobjects(authid,host).keys():
            print "%s is already exists" % host
            return False

        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "template.create",
                "params": {
                    "host": host,
                    "groups": {
                        "groupid": groups
                    }

                },
                "auth": self.authid,
                "id": 1
            })

        try:
            response = requests.get(self.url,data=data,headers=self.header)
            return response.json()['result']['templateids']
        except KeyError as e:
            print "params Error! 请检查!"
            return None

    def hostgroup_get(self):
        ''' 获取用户组ID '''
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": "extend",
                },
                "auth": self.authid,
                "id": 1
            })

        hostgroups = {}
        response = requests.get(self.url,data=data,headers=self.header)

        for result in response.json()['result']:
            hostgroups[result['name']] = result['groupid']
            return hostgroups

    def hostgroup_filter(self,*groupname):
        ''' 获取用户组ID '''
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": "extend",
                    "filter": {
                        "name":
                        groupname,
                    }
                },
                "auth": self.authid,
                "id": 1
            })

        hostgroups = {}
        response = requests.get(self.url,data=data,headers=self.header)
        for result in response.json()['result']:
            hostgroups[result['name']] = result['groupid']

        return hostgroups

    def hostgroup_create(self,name):
        '''创建主机组 name最好不要为中文'''
        if name in self.hostgroup_filter(name).keys():
            print "hostgroup already exist."
            return False

        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": name,
            },
            "auth": self.authid,
            "id": 1
        })

        response = requests.get(self.url,data=data,headers=self.header)

        try:
            return response.json()['result']['groupids']
        except KeyError as e:
            print response.json()['error']
            return None

    def _host_exists(self,host):
        '''host 为template里的HOST NAME'''
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.exists",
                "params": {
                    "host": host,
                },
                "auth": self.authid,
                "id": 1
            })

        response = requests.get(self.url,data=data,headers=self.header)
        return response.json()['result']

    def host_filter(self,*hostip):
        '''host: HOST NAME
        获取hostid
        '''
        data = json.dumps({

            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                # "output": "extend",
                "output": ["hostid"],
                "filter": {
                    "host": hostip,
                }
            },
            "auth": self.authid,
            "id": 1
        })

        response = requests.get(self.url,data=data,headers=self.header)
        print response.json()
        return response.json()['result']

    def host_get(self):
        '''host 为template里的HOST NAME'''
        data = json.dumps({

            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                # "output": "extend",
                "output": ["hostid","host","status"],
                # "filter": {
                #     "host": host,
                # }
            },
            "auth": self.authid,
            "id": 1
        })

        response = requests.get(self.url,data=data,headers=self.header)

        return response.json()['result']

    def host_create(self,host,groupid,ip,templateid,port=10050):
        ''' authid: 登录秘钥
        host: HOST Name
        groupid: Host groups 的ID,可以为列表
        ip: ip地址
        templateid: templates的id,可以为列表
        port: 默认为10050
        '''
        if self._host_exists(host):
            print "Host %s already exist." % (host)
            return False

        groups = []
        if type(groupid) == list:
            for gid in groupid:
                groups.append({"groupid":gid})
        else:
            groups.append({"groupid": groupid})

        templates = []
        if type(templateid) == list:
            for tid in templateid:
                templates.append({"templateid":tid})
        else:
            templates.append({"templateid": templateid})

        ''' 创建host '''
        data = json.dumps ({
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": host,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": "",
                        "port": port
                    }
                ],
                "groups": groups,
                "templates": templates,
            },
            "auth": self.authid,
            "id": 1
        })

        try:
            response = requests.get(self.url,data=data,headers=self.header)
            print response.json()
            return response.json()['result']['hostids']
        except KeyError as e:
            print "params Error! 请检查!"
            return None

    def _screen_exists(self,name):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "screen.exists",
            "params": {
                "name": name
            },
            "auth": self.authid,
            "id": 1
        })

        response = requests.post(self.url,data=data,headers=self.header)
        return response.json()['result']

    def screen_get(self,name):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "screen.get",
            "params": {
                "output": "extend",
                # "selectScreenItems": "screenid",
                "preservekeys": True,
                # "limit": 1,
                "filter":{
                    "name": name,

                }
            },

            "auth": self.authid,
            "id": 1
        })

        response = requests.post(self.url,data=data,headers=self.header)
        print response.json()
        # 返回结果 {u'jsonrpc': u'2.0', u'result': {u'22': {u'name': u'\u963f\u91cc\u4e91\u6d41\u91cf\u76d1\u6d4b', u'hsize': u'2', u'screenid': u'22', u'screenitems': [], u'templateid': u'0', u'vsize': u'8'}}, u'id': 1}
        return response.json()['result'].keys()

    def screen_creat(self,name):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "screen.create",
            "params": {
                "name": "Graphs",
                "hsize": 3,
                "vsize": 2,
                "screenitems": [
                    {
                        "resourcetype": 0,
                        "resourceid": "612",
                        "rowspan": 0,
                        "colspan": 0,
                        "x": 0,
                        "y": 0
                    }
                ]
            },
            "auth": self.authid,
            "id": 1
        })

    def host_create_link_template(self):

        parser = argparse.ArgumentParser(description=u"创建一个自动链接好模板的host",usage="Prog [options]")
        parser.add_argument("-g","--hostgroup",help=u'属于哪个用户组')
        parser.add_argument("-n","--hostname",help=u'zabbix显示的主机名')
        parser.add_argument("-i","--ip",help=u'zabbix要添加的主机的IP')
        parser.add_argument("-t","--templatename",help=u"此主机需要链接的模板名字")

        args = parser.parse_args()
        hostgroup = args.hostgroup
        hostname = args.hostname
        ip = args.ip
        templatename = args.templatename.split(',')

        api = Zabbix_Api()
        gid = api.hostgroup_filter(hostgroup).values()
        tids = api.template_getobjects(templatename).values()
        api.host_create(hostname,gid,ip,tids)

if __name__ == "__main__":
    api = Zabbix_Api()

    #gid=api.hostgroup_filter('Zabbix servers')
    # print gid.values()
    #tid=api.template_getobjects('APP_TOMCAT_CPU_MONITOR','Template ICMP Ping','Template Linux DiskIO','Server performance')
    #print tid.values()

    # api.hostgroup_create('warfare_3ken_server')
    # api.host_create('manager_104.154',gid.values(),'38.123.104.154',tid.values())

    #print api.screen_get("阿里云流量监测")
    #gid1=api.hostgroup_filter('Zabbix servers')
    api.host_create_link_template()
