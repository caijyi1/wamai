#!/bin/bash

set -e
source /data/save/make_logs

: ${3?"Usage $0 平台ID 平台名 游戏服,Example $0 15 wabao s1"}

_MYSQLBIN="/usr/local/db1/bin/mysql -sBNc -h127.0.0.1 -uroot -p`cat /data/save/mysql_root` wabao_center"

function T_or_F() {
    [[ $? -eq 0 ]] && save_logs  -green ${1}_成功 |tee -a install_server_log || save_logs -red ${1}_失败 |tee -a install_server_log
}

function get_help(){
	${_MYSQLBIN} -e "select  a.sPlatName,a.iProjectId,b.sProjectName \
	from cloud_plat_server a join project b on b.iProjectId = a.iProjectId
	group by a.sPlatName,a.iProjectId;"
}

function base_config {
    mkdir -p /data/backup/{database,Server}/
    #拉取中心监控脚本目录
    mkdir -p /data/sh/
    scp -P $port $fserver:/data/sh/*  /data/sh/
    scp -P $port $fserver:/etc/crontab /etc/
    [ -d '/data/sh/switch/status/' ] && { /bin/rm -rf /data/sh/switch/status/* ; }
}

function initalize() {
    Project=$2
    server=$3
    server_flag=$2_$3
    if [[ $Project == "wabao" ]];then
        fserver=114.55.172.25
        fserver_flag=wabao_s5
        carduser=114.55.11.191
        port=22
        logdbip=10.26.249.17
    elif  [[ $Project == "lianyun" ]]; then
        fserver=114.55.174.126
        fserver_flag=lianyun_s6001
        carduser=114.55.11.191
        port=22
        logdbip=10.26.249.17
    elif [[ $Project == "fanti" ]]; then
        fserver=119.28.61.214
        fserver_flag=fanti_s1
        carduser=119.28.19.229
        port=22
        logdbip=10.144.80.164
    elif [[ $Project == "en" ]]; then
        fserver=107.150.97.198
        fserver_flag=en_s1
        carduser=107.150.97.160
        port=36000
        logdbip=10.11.39.241
    else [[ $Project == "dewen" ]];
        fserver=35.156.203.239
        fserver_flag=dewen_s1
        carduser=35.156.104.76
        port=36000
        logdbip=10.20.33.132
    fi


    serverip=$(${_MYSQLBIN} -e "select sIPCtcc from cloud_plat_server where iProjectId=$1 and sPlatName='$Project' group by sIPCtcc order by count(sIPCtcc) limit 1;")
    if [[ $Project == "wabao" ]]; then
        Dbip=$(${_MYSQLBIN} -e "select sDBIP from cloud_plat_server where iProjectId=$1 and sPlatName='$Project' and sDBIP!='rm-bp1l98mo3z7j1jz8l.mysql.rds.aliyuncs.com' group by sDBIP order by count(sDBIp) limit 1;")
    else
       Dbip=$(${_MYSQLBIN} -e "select sDBIP from cloud_plat_server where iProjectId=$1 and sPlatName='$Project' group by sDBIP order by count(sDBIp) limit 1;")
    fi

    check_domain
    check_server

    source_gdbip=$(ssh -p $port ${fserver} "grep \"db.game.url\" /app/warfare/${fserver_flag}/gameServer/config/game.properties | sed 's#.*mysql://\(.*\):3306/.*#\1#g'")
    source_logdbip=$(ssh -p $port ${fserver} "grep \"db.log.url\" /app/warfare/${fserver_flag}/gameServer/config/game.properties | sed 's#.*mysql://\(.*\):3306/.*#\1#g'")
    source_cdbip=$(ssh -p $port ${fserver} "grep \"db.config.url\" /app/warfare/${fserver_flag}/gameServer/config/game.properties | sed 's#.*mysql://\(.*\):3306/.*#\1#g'")

    echo -e "\033[36mserverip:$serverip\nserver_flag:${server_flag}\nDbip:$Dbip\nsource_cdbip:${source_cdbip}\nsource_gdbip:${source_gdbip}\nsource_logdbip:${source_logdbip}\033[0m" |tee install_server_log
    echo -e "\033[36mlogdbip:$logdbip\nport:$port\ncarduser:$carduser\nfserver_flag:$fserver_flag\nfserver:$fserver\033[0m" |tee -a install_server_log
    #MPORT=$(ssh -p $port $serverip ss -tunlp |grep java |awk  -F'[: ]+' '{print $6|"sort -rn"}'|head -1)
    MPORT=$(ssh -p $port $serverip "find /app/warfare/ -name 'game.properties' | xargs grep 'game.web.port='"| awk -F'=' '{print $NF|"sort"}'|tail -1)
    if [[ "x$MPORT" != "x" ]];then
        GAMEPORT=$(($MPORT+1))
        WEBPORT=$(($MPORT+2))
    else
        GAMEPORT=6001
        WEBPORT=6002
    fi
    GAMEID=$(echo $server |tr -d "s")
    echo -e "\033[36mGAMEID:$GAMEID\nGAMEPORT:$GAMEPORT\nWEBPORT:$WEBPORT\nMPORT:$MPORT\nDOMAIN_NAME:${DOMAIN_NAME}\033[0m" |tee -a install_server_log
}

function check_server() {
    save_logs -yellow "($serverip)连接测试,请稍候..." | tee -a install_server_log
    ins=$(ssh -p $port $serverip "ls /app/warfare/${server_flag}/gameServer/ | wc -l")
    [[ -z "${ins}" ]] && save_logs -red "($serverip)无法连接,脚本退出..." | tee -a install_server_log && exit 1
    if [[ $ins -eq 0 ]];then
        save_logs -yellow "($serverip) (${server_flag})游戏程序不存在,可以进行安装..." | tee -a install_server_log
    else
        save_logs -red "($serverip)游戏程序已存在，请检查配置参数是否正确，脚本退出..." | tee -a install_server_log
        exit 1
    fi
}

function check_domain() {
    if [[ $Project == "wabao" ]] || [[ $Project == "lianyun" ]]; then
        DOMAIN_NAME=$(cat /etc/hosts|grep ${serverip} |awk '{print $2}')
        if [[ -z "${DOMAIN_NAME}" ]]; then
            save_logs -red "${DOMAIN_NAME}" 不存在 && exit 1
        fi
    fi
}

function rds() {
    #创建数据库
    aliDB=${Dbip%%.*}
    aliyuncli rds CreateDatabase --DBInstanceId $aliDB --DBName configdb_${server_flag} --CharacterSetName utf8mb4
    T_or_F "configdb_${server_flag}_创建"
    aliyuncli rds CreateDatabase --DBInstanceId $aliDB --DBName gamedb_${server_flag} --CharacterSetName utf8mb4
    T_or_F "gamedb_${server_flag}_创建"

    sleep 60
    aliyuncli rds GrantAccountPrivilege --DBName configdb_${server_flag} --DBInstanceId $aliDB --AccountName wabao_game --AccountPrivilege ReadWrite
    T_or_F "configdb_${server_flag}_授权—wabao_game"
    aliyuncli rds GrantAccountPrivilege --DBName configdb_${server_flag} --DBInstanceId $aliDB --AccountName wabao_config --AccountPrivilege ReadWrite
    T_or_F "configdb_${server_flag}_授权—wabao_config"
    aliyuncli rds GrantAccountPrivilege --DBName configdb_${server_flag} --DBInstanceId $aliDB --AccountName dev_check --AccountPrivilege ReadOnly
    T_or_F "configdb_${server_flag}_授权—dev_check"

    aliyuncli rds GrantAccountPrivilege --DBName gamedb_${server_flag} --DBInstanceId $aliDB --AccountName wabao_game --AccountPrivilege ReadWrite
    T_or_F "gamedb_${server_flag}_授权—wabao_game"
    aliyuncli rds GrantAccountPrivilege --DBName gamedb_${server_flag} --DBInstanceId $aliDB --AccountName wabao --AccountPrivilege ReadOnly
    T_or_F "gamedb_${server_flag}_授权—wabao"
    aliyuncli rds GrantAccountPrivilege --DBName gamedb_${server_flag} --DBInstanceId $aliDB --AccountName dev_check --AccountPrivilege ReadOnly
    T_or_F "gamedb_${server_flag}_授权—dev_check"
}

function local_mysql() {
    ssh -p $port $serverip "/usr/local/db1/bin/mysqladmin -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} ping"|grep -qw 'alive'
    T_or_F "游戏数据库${Dbip}_连接"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} \
        -e 'CREATE DATABASE configdb_${server_flag} DEFAULT CHARACTER SET utf8mb4;'"
    T_or_F "configdb_${server_flag}_创建"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} \
        -e 'CREATE DATABASE gamedb_${server_flag} DEFAULT CHARACTER SET utf8mb4;'"
    T_or_F "gamedb_${server_flag}_创建"

    #授权数据库
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} \
        -e 'grant all privileges on configdb_${server_flag}.* to wabao_game@\"%\";'"
    T_or_F "configdb_${server_flag}_授权—wabao_game"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} \
        -e 'grant all privileges on configdb_${server_flag}.* to wabao_config@\"%\"; flush privileges'"
    T_or_F "configdb_${server_flag}_授权—wabao_config"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} \
        -e 'grant select on configdb_${server_flag}.* to dev_check@\"%\"; flush privileges'"
    T_or_F "configdb_${server_flag}_授权—dev_check"

    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} \
        -e 'grant all privileges on gamedb_${server_flag}.* to wabao_game@\"%\";'"
    T_or_F "configdb_${server_flag}_授权—wabao_game"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} \
        -e 'grant select on gamedb_${server_flag}.* to wabao@\"%\"; flush privileges'"
    T_or_F "gamedb_${server_flag}_授权—wabao"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${Dbip} \
        -e 'grant select on gamedb_${server_flag}.* to dev_check@\"%\"; flush privileges'"
    T_or_F "gamedb_${server_flag}_授权—dev_check"
}

function logdb() {
    #创建数据库
    ssh -p $port $serverip "/usr/local/db1/bin/mysqladmin -uroot -p`cat /data/save/$Project/mysql_root` -h${logdbip} ping"|grep -qw 'alive'
    T_or_F "日志数据库${logdbip}_连接"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${logdbip} \
        -e 'create database gamelog_${server_flag} default character set utf8mb4;'"
    T_or_F "gamelog_${server_flag}_创建"
    #授权数据库
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${logdbip} \
        -e 'grant all privileges on gamelog_${server_flag}.* to wabao_game@\"%\";'"
    T_or_F "gamelog_${server_flag}_授权—wabao_game"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${logdbip} \
        -e 'grant select on gamelog_${server_flag}.* to wabao@\"%\"; flush privileges'"
    T_or_F "gamelog_${server_flag}_授权—wabao"
    ssh -p $port $serverip "/usr/local/db1/bin/mysql -uroot -p`cat /data/save/$Project/mysql_root` -h${logdbip} \
        -e 'grant select on gamelog_${server_flag}.* to dev_check@\"%\"; flush privileges'"
    T_or_F "gamelog_${server_flag}_授权—dev_check"
}

function rsync_gs() {
    #[[ GAMEPORT -eq 6001 ]] && save_logs -red "第一次装服,请做好预备工作" |tee -a install_server_log
    ssh -p $port $serverip "touch /data/sh/switch/status/${server_flag}.txt"
    ssh -p $port $serverip ">/data/sh/switch/status/${server_flag}.txt"
    rsync -aqcz  --delete -e "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=60 -p ${port}" \
    --exclude='*.tar.gz*' --exclude='.svn/' --exclude='*.swp' --exclude='*.swo' --exclude='logs/*' --exclude='null'  \
    root@$fserver:/app/warfare/${fserver_flag}/gameServer  /data/tmp/${server_flag}/
    T_or_F "从${fserver}拉取文件到本地_"
    rsync -avcz /data/tmp/${server_flag} $serverip:/app/warfare/
    T_or_F "游戏服${server_flag}推送到${serverip}_"
}

function properties_config() {
    ssh -p $port ${serverip} "sed -i 's#\(game.id=\).*#\1${GAMEID}#g' /app/warfare/${server_flag}/gameServer/config/game.properties"
    ssh -p $port ${serverip} "sed -i 's#\(game.port=\).*#\1${GAMEPORT}#g' /app/warfare/${server_flag}/gameServer/config/game.properties"
    ssh -p $port ${serverip} "sed -i 's#\(web.port=\).*#\1${WEBPORT}#g' /app/warfare/${server_flag}/gameServer/config/game.properties"
#修改连接数据库相关信息
    ssh -p $port ${serverip} "sed -ri 's#${fserver_flag}#${server_flag}#g' /app/warfare/${server_flag}/gameServer/config/game.properties"
    ssh -p $port ${serverip} "sed -ri 's#(db.game.url.*)${source_gdbip}(:3306.*)#\1${Dbip}\2#g' /app/warfare/${server_flag}/gameServer/config/game.properties"
    ssh -p $port ${serverip} "sed -ri 's#(db.config.url.*)${source_cdbip}(:3306.*)#\1${Dbip}\2#g' /app/warfare/${server_flag}/gameServer/config/game.properties"
    ssh -p $port ${serverip} "sed -ri 's#(db.log.url.*)${source_logdbip}(:3306.*)#\1${logdbip}\2#g' /app/warfare/${server_flag}/gameServer/config/game.properties"
    T_or_F "配置文件修改_"
#添加防火墙
    ssh -p $port ${serverip} "sed -i \"/ 22 /a-A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport ${GAMEPORT} -j ACCEPT\" /etc/sysconfig/iptables"
    ssh -p $port ${serverip} "sed -i \"/ 22 /a-A RH-Firewall-1-INPUT -s ${carduser} -p tcp -m state --state NEW -m tcp --dport ${WEBPORT} -j ACCEPT\" /etc/sysconfig/iptables"
    ssh -p $port ${serverip} "service iptables reload"
    T_or_F "防火墙修改_"

}

function dbconn() {
    save_logs -yellow "正在测试连接configdb数据库..." |tee -a install_server_log
    result=0
    while [[ "x$result" != "x1" ]]
    do
        sleep 15
        result=$(ssh -p $port $serverip "/usr/local/db1/bin/mysql -BNc -uwabao_game -p`cat /data/save/$Project/mysql_wabao_game` -h${Dbip} configdb_${server_flag} -e 'select 1'")
        #result=$(ssh 114.55.237.41 "/usr/local/db1/bin/mysql -BNc -uwabao_game -p`cat /data/save/$Project/mysql_wabao_game` -hrm-bp190565h9s2om3i0.mysql.rds.aliyuncs.com configdb_wabao_s113 -e 'select 1'")
        T_or_F "${Dbip} wabao_game configdb_${fserver_flag}连接_"
    done
}

function import_configdb() {
    save_logs -yellow "正在导入configdb数据..."|tee -a install_server_log
    ssh -p $port $serverip "/usr/local/db1/bin/mysqldump -uwabao_game -p`cat /data/save/$Project/mysql_wabao_game` -h${source_cdbip} \
    --default-character-set=utf8 --set-gtid-purged=OFF --single-transaction configdb_${fserver_flag} | \
    /usr/local/db1/bin/mysql -BNc -uwabao_game -p`cat /data/save/$Project/mysql_wabao_game` -h${Dbip} configdb_${server_flag}"
    T_or_F "${Dbip} wabao_game ${fserver_flag}导入_"
}

function add_opcenter {
    #加入账号服，合服或者切机返回1则为正常，否则错误，测试中央服
    ssh -p $port ${carduser} "sh /data/sh/addwarfare/wabao_warfare_cloud_add_center.sh $Project ${server} ${serverip} ${Dbip} ${GAMEPORT} ${WEBPORT} ${GAMEID} ${DOMAIN_NAME}"
    echo -e "sh /data/sh/addwarfare/wabao_warfare_cloud_add_center.sh $Project ${server} ${serverip} ${Dbip} ${GAMEPORT} ${WEBPORT} ${GAMEID} ${DOMAIN_NAME}"
    sh /data/sh/addGame/wabao_cloud_interface_addServer.sh $Project ${server} ${Dbip} ${serverip} $1
    echo "sh /data/sh/addGame/wabao_cloud_interface_addServer.sh $Project ${server} ${Dbip} ${serverip} $1"
}

function handle_database() {
    if [[ $Project == "wabao" ]] || [[ $Project == "lianyun" ]];
        then
        rds
        logdb
    else
        local_mysql
        logdb
    fi
}

function main() {
    initalize $1 $2 $3
    read -p "`echo -e \"\033[1;31m 确认要根据以上配置进行装服吗？【Y/N】：\033[0m\"`" Y
    case $Y in
        yes|y|Y)
            handle_database
            rsync_gs
            properties_config
            dbconn
            import_configdb
            add_opcenter $1
            ;;
        no|n|N)
            exit 0
            ;;
        *)
            continue
            ;;
    esac

save_logs -yellow "游戏安装已完成，本次安装花时:\"$SECONDS\"秒" | tee -a install_server_log
save_logs -yellow "请执行开启游戏：ssh -p $port $serverip sh /data/sh/switch/start_game.sh ${server_flag}" |tee -a install_server_log
}

main $1 $2 $3
