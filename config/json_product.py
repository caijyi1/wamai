#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb
import json
import collections
import pprint

def productfile(mold,proid,name):
    if mold == 'info':
        cur_col = 'sIPCtcc'
    else:
        cur_col = 'sDBIp'

    cursor.execute("""
                   select %s,group_concat(concat(sPlatName,'_',sPlatServer))
                   from cloud_plat_server where iProjectId = %d and sPlatName = '%s' group by %s;
                   """ % (cur_col,proid,name,cur_col))

    rows = cursor.fetchall()
    javas={}
    for row in rows:
        javas[list(row)[0]]=list(row)[1].split(',')

    j = json.dumps(javas)

    if proid == 15 and name == 'wabao':
        json_file = 'jdfbserver_%s.js' % mold
    elif proid == 6:
        json_file = 'kzdgserver_%s.js' % mold
    else:
        json_file = '%sserver_%s.js' % (name,mold)

    pprint.pprint(j)
    with open(json_file,'w') as f:
        f.write(j)


if __name__ == '__main__':
    db = MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='wabao*@#1AF2330?airfight',db='wabao_center',charset='utf8')
    cursor = db.cursor()
    #-------生成js文件
    # 绝地风暴
    #productfile('db',15,'wabao')
    productfile('info',15,'wabao')

    #productfile('db',15,'lianyun')
    productfile('info',15,'lianyun')

    #productfile('db',18,'fanti')
    productfile('info',18,'fanti')

    #productfile('db',19,'dewen')
    #productfile('info',19,'dewen')

    #productfile('db',20,'en')
    #productfile('info',20,'en')

    cursor.close()
    db.close()
