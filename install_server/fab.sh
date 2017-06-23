#描述db状态
aliyuncli rds DescribeDBInstances --DBInstanceId rds1rko9q83dzi85r9n0
#cdn域名信息
aliyuncli CDN DescribeCdnDomainBaseDetail --DomainName zzskcdn.tmsjyx.com
#cdn刷新缓存
TASKID=aliyuncli cdn RefreshObjectCaches --ObjectType Directory --ObjectPath "zzskcdn.tmsjyx.com/apk/cn_android/packver_7/" |grep -Po '(?<="RefreshTaskId": )".*"'
aliyuncli cdn DescribeRefreshTasks --TaskId ${TASKID} |grep -Po '(?<="Process": )"[0-9]+%"'
