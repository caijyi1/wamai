#描述db状态
#aliyuncli rds DescribeDBInstances --DBInstanceId rds1rko9q83dzi85r9n0
#cdn域名信息
#aliyuncli CDN DescribeCdnDomainBaseDetail --DomainName zzskcdn.tmsjyx.com
#cdn刷新缓存
#TASKID=aliyuncli cdn RefreshObjectCaches --ObjectType Directory --ObjectPath "zzskcdn.tmsjyx.com/apk/cn_android/packver_7/" |grep -Po '(?<="RefreshTaskId": )".*"'
#aliyuncli cdn DescribeRefreshTasks --TaskId ${TASKID} |grep -Po '(?<="Process": )"[0-9]+%"'

#aliyuncli cdn RefreshObjectCaches --ObjectType Directory --ObjectPath "kzdgcdn.tmsjyx.cn/zone_20043/"
#aliyuncli cdn RefreshObjectCaches --ObjectType Directory --ObjectPath "kzdgcdn.tmsjyx.cn/zone_30000/"
#aliyuncli cdn RefreshObjectCaches --ObjectType Directory --ObjectPath "kzdgcdn.tmsjyx.cn/all/"

function rmdb(){
aliyuncli rds DeleteDatabase --DBInstanceId ${1} --DBName ${2}
sleep 20
}

function createdb(){
aliyuncli rds CreateDatabase --DBInstanceId ${1} --DBName ${2} --CharacterSetName utf8mb4
sleep 15
}

function grantdb() {
aliyuncli rds GrantAccountPrivilege --DBName ${2} --DBInstanceId ${1} --AccountName wabao_game --AccountPrivilege ReadWrite   
aliyuncli rds GrantAccountPrivilege --DBName ${2} --DBInstanceId ${1} --AccountName wabao --AccountPrivilege ReadOnly  
aliyuncli rds GrantAccountPrivilege --DBName ${2} --DBInstanceId ${1} --AccountName dev_check --AccountPrivilege ReadOnly
}

#rmdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8016
#rmdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8017
#rmdb rm-bp113c892je5m2nl5	warfare_cross_s8018
#rmdb rm-bp113c892je5m2nl5	warfare_cross_s8019
#rmdb rm-bp113c892je5m2nl5	warfare_cross_s8020
#rmdb rm-bp113c892je5m2nl5	warfare_cross_s8021
#rmdb rm-bp113c892je5m2nl5	warfare_cross_s8022
#rmdb rm-bp113c892je5m2nl5	warfare_cross_s8023
#rmdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8000
#rmdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8001
#rmdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8002
#rmdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8003
#rmdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8004
#rmdb rm-bp1jy7014lldsvu6b	warfare_cross_s8005
#rmdb rm-bp1jy7014lldsvu6b	warfare_cross_s8006
#rmdb rm-bp1jy7014lldsvu6b	warfare_cross_s8007
#rmdb rm-bp1jy7014lldsvu6b	warfare_cross_s8008
#rmdb rm-bp1jy7014lldsvu6b	warfare_cross_s8009
rmdb rm-bp100jph5rpdazs9n	warfare_cross_s8010
rmdb rm-bp100jph5rpdazs9n	warfare_cross_s8011
rmdb rm-bp100jph5rpdazs9n	warfare_cross_s8012
#rmdb rm-bp100jph5rpdazs9n	warfare_cross_s8013
#rmdb rm-bp100jph5rpdazs9n	warfare_cross_s8014
#rmdb rm-bp100jph5rpdazs9n	warfare_cross_s8015


#createdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8016
#createdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8017
#createdb rm-bp113c892je5m2nl5	warfare_cross_s8018
#createdb rm-bp113c892je5m2nl5	warfare_cross_s8019
#createdb rm-bp113c892je5m2nl5	warfare_cross_s8020
#createdb rm-bp113c892je5m2nl5	warfare_cross_s8021
#createdb rm-bp113c892je5m2nl5	warfare_cross_s8022
#createdb rm-bp113c892je5m2nl5	warfare_cross_s8023
#createdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8000
#createdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8001
#createdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8002
#createdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8003
#createdb rm-bp11a0ajbf7zob7dy	warfare_cross_s8004
#createdb rm-bp1jy7014lldsvu6b	warfare_cross_s8005
#createdb rm-bp1jy7014lldsvu6b	warfare_cross_s8006
#createdb rm-bp1jy7014lldsvu6b	warfare_cross_s8007
#createdb rm-bp1jy7014lldsvu6b	warfare_cross_s8008
#createdb rm-bp1jy7014lldsvu6b	warfare_cross_s8009
createdb rm-bp100jph5rpdazs9n	warfare_cross_s8010
createdb rm-bp100jph5rpdazs9n	warfare_cross_s8011
createdb rm-bp100jph5rpdazs9n	warfare_cross_s8012
#createdb rm-bp100jph5rpdazs9n	warfare_cross_s8013
#createdb rm-bp100jph5rpdazs9n	warfare_cross_s8014
#createdb rm-bp100jph5rpdazs9n	warfare_cross_s8015


#grantdb rm-bp11a0ajbf7zob7dy  warfare_cross_s8016
#grantdb rm-bp11a0ajbf7zob7dy  warfare_cross_s8017
#grantdb rm-bp113c892je5m2nl5  warfare_cross_s8018
#grantdb rm-bp113c892je5m2nl5  warfare_cross_s8019
#grantdb rm-bp113c892je5m2nl5  warfare_cross_s8020
#grantdb rm-bp113c892je5m2nl5  warfare_cross_s8021
#grantdb rm-bp113c892je5m2nl5  warfare_cross_s8022
#grantdb rm-bp113c892je5m2nl5  warfare_cross_s8023
#grantdb rm-bp11a0ajbf7zob7dy  warfare_cross_s8000
#grantdb rm-bp11a0ajbf7zob7dy  warfare_cross_s8001
#grantdb rm-bp11a0ajbf7zob7dy  warfare_cross_s8002
#grantdb rm-bp11a0ajbf7zob7dy  warfare_cross_s8003
#grantdb rm-bp11a0ajbf7zob7dy  warfare_cross_s8004
#grantdb rm-bp1jy7014lldsvu6b  warfare_cross_s8005
#grantdb rm-bp1jy7014lldsvu6b  warfare_cross_s8006
#grantdb rm-bp1jy7014lldsvu6b  warfare_cross_s8007
#grantdb rm-bp1jy7014lldsvu6b  warfare_cross_s8008
#grantdb rm-bp1jy7014lldsvu6b  warfare_cross_s8009
grantdb rm-bp100jph5rpdazs9n   warfare_cross_s8010
grantdb rm-bp100jph5rpdazs9n   warfare_cross_s8011
grantdb rm-bp100jph5rpdazs9n   warfare_cross_s8012
#grantdb rm-bp100jph5rpdazs9n  warfare_cross_s8013
#grantdb rm-bp100jph5rpdazs9n  warfare_cross_s8014
#grantdb rm-bp100jph5rpdazs9n  warfare_cross_s8015
