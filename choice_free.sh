#!/bin/bash

#get host or db

#: ${2?"Usage $0 iProjectId splatName,example $0 15 wabao `get_help`"}


_MYSQLBIN="/usr/local/db1/bin/mysql -sBNc -h127.0.0.1 -uroot -p`cat /data/save/mysql_root` wabao_center"

function get_help(){
	#${_MYSQLBIN} -e "select count(a.sPlatName) AS "游戏服总数", a.sPlatName,a.iProjectId,b.sProjectName \
	${_MYSQLBIN} -e "select  a.sPlatName,a.iProjectId,b.sProjectName \
	from cloud_plat_server a join project b on b.iProjectId = a.iProjectId 
	group by a.sPlatName,a.iProjectId;"
}

function get_host(){
    serverip=$(${_MYSQLBIN} -e "select sIPCtcc from cloud_plat_server where iProjectId=$1 and sPlatName='$2' group by sIPCtcc order by count(sIPCtcc) limit 1;")
    Dbip=$(${_MYSQLBIN} -e "select sDBIP from cloud_plat_server where iProjectId=$1 and sPlatName='$2' group by sDBIP order by count(sDBIp) limit 1;")
}

#get_help
: ${2?"Usage $0 iProjectId platName,Example $0 15 wabao"}
get_host $1 $2
echo $serverip
echo $Dbip
