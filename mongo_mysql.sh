#!/bin/bash

mongoexport --host 127.0.0.1:27017 --username wabao_user --password YzrSaODnXQuaYlwGBbU2 -d sanguouser -c role --type=csv -f _id,account,aid,channelId,createTime,expand,level,loginTime,logoutTime,name,serverId,vip -o /tmp/role.csv
#
### 数据模板如下# head -2 /tmp/role.csv 
### _id,account,aid,channelId,createTime,expand,level,loginTime,logoutTime,name,serverId,vip
### 1,p01249609h,1000002,10000,2017-06-09 09:40:51,json,60,2017-04-28 10:35:41,2017-06-09 09:41:26,弘子敕,1,0
##
sed -ri 's/(20.*)T(.*)(\..*)Z/\1 \2/g' /tmp/role.csv
sed -ri 's/(20.*)T(.*)(\..*)Z/\1 \2/g' /tmp/role.csv
sed -ri 's/(20.*)T(.*)(\..*)Z/\1 \2/g' /tmp/role.csv
sed -ri 's/(20.*)T(.*)(\..*)Z/\1 \2/g' /tmp/role.csv
#
/usr/local/db1/bin/mysql -uroot -p`cat /data/save/mysql_root` -h127.0.0.1  test -e  "truncate role;"
/usr/local/db1/bin/mysql -uroot -p`cat /data/save/mysql_root` -h127.0.0.1  test -f -e "load data infile '/tmp/role.csv' into table role character set utf8 fields terminated by ',' lines terminated by '\n' ignore 1 lines
(_id,account,aid,channelId,createTime,expand,level,loginTime,@logoutTime,name,serverId,vip)
set logoutTime=if(@logoutTime='',loginTime,@logoutTIme)"
/usr/local/db1/bin/mysql -uroot -p`cat /data/save/mysql_root` -h127.0.0.1  test -f -e "UPDATE role SET createTime = DATE_ADD(createTime, INTERVAL 8 HOUR),loginTime = DATE_ADD(loginTime, INTERVAL 8 HOUR),logoutTime = DATE_ADD(logoutTime, INTERVAL 8 HOUR);"


