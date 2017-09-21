#!/usr/bin/env python
#-*- coding:utf8 -*-

from fabric.colors import *
import os,logging,sys,json
import logging.handlers
import ConfigParser
from fabric.api import *

reload(sys)
sys.setdefaultencoding('utf-8')


CFILE = "config/config.ini"


class Config:

    def __init__(self,cfile):
        self.cfile = cfile
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(self.cfile)

        self.actime = self.cfg.get('global','actime')
        self.dbname = self.cfg.get('config_sql','dbname')
        self.ignore = self.cfg.get('config_sql','igtables')

        self.dbuser = 'wabao'
        self.dbpasswd = 'wabao*330?*@hero'
        #内网72的IP为125.88.171.116
        self.host = '125.88.171.116'
        self.tables = self.cfg.get('config_sql','table')

        self.querysqls = self.cfg.get('gamedb_sql','querysql')

        self.project = self.cfg.get('game','project')
        self.java_us = self.cfg.get('game','java_u').replace("\"","")
        self.paths = self.cfg.get('game','paths')
        self.c_config = self.cfg.get('game','c_config')


    def get_java(self):
        javas=[]
        x=[]
        for i in self.java_us.split(","):
            if '-' not in i:
                javas.append(i)
                continue
            else:
                x.append(i.split("-"))

        for j in x:
            for k in range(int(j[0].split('_s')[1]), int(j[1].split('_s')[1])+1):
                java="%s_s%s" %(j[0].split('_s')[0],k)
                javas.append(java)

        return javas
    # return list(set(javas)) 去重

    def getdbdump(self):
        if self.ignore.lower() == "yes":
            self.dbdump = "/usr/local/db1/bin/mysqldump -u%s -p%s -h%s %s --ignore-table=%s.activity_operation --ignore-table=%s.activity_notice --ignore-table=%s.cross_init --ignore-table=%s.activity_params >%s/gameServer/configdb_release.sql" % (self.dbuser,self.dbpasswd,self.host,self.dbname,self.dbname,self.dbname,self.dbname,self.dbname,env.lpath)
            #self.dbdump = "/usr/local/db1/bin/mysqldump -u%s -p%s -h%s %s --ignore-table=%s.activity_operation --ignore-table=%s.activity_notice >%s/gameServer/configdb_release.sql" % (self.dbuser,self.dbpasswd,self.host,self.dbname,self.dbname,self.dbname,env.lpath)
        else:
            self.dbdump = ("/usr/local/db1/bin/mysqldump -u%s -p%s -h%s %s %s >%s/gameServer/configdb_release.sql") % (self.dbuser,self.dbpasswd,self.host,self.dbname,self.tables.replace(","," "),env.lpath)

        return self.dbdump

parser=Config(CFILE)
if not parser.project:
    print "project 为必填项！请检查配置文件.."
    sys.exit(1)

def initLoggerWithRotate():
    logpath = "/tmp"
    logfile = "fabfile_%s%s.log" %(parser.actime,parser.project)

    if not os.path.exists(logpath):
        os.mkdirs(logpath)
    else:
        logfile = os.path.join(logpath,logfile)

    logger = logging.getLogger("fabric")
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger

logger = initLoggerWithRotate()


def jsonload(f):
    with open(f,'r') as json_file:
        data=json.load(json_file)

    return data

#servers_db 每台数据库分别存放了哪些游戏服的库
#servers_java 每台服务器上分别存放了哪些游戏服
servers_java = jsonload("config/%sserver_info.js" %parser.project)
#归总所有的项目数据库密码
env.dbpassword = jsonload("config/sqlpasswd.js")[parser.project.strip()]

env.lpath = "/data/update_warfare/%s_%s" %(parser.actime,parser.project)

env.roledefs = {
    'sourceserver': ['root@125.88.171.116:9821'],
    parser.project + "game" : servers_java.keys(),
}

java_u = parser.get_java()
print cyan(env.roledefs)
print magenta(java_u)
print magenta(parser.paths)
print red(parser.querysqls.replace(';',';\r\n'))

if parser.project in ['en','dewen']:
    env.port = 36000
else:
    env.port = 22

env.dbuser="wabao_game"


env.user="root"
env.sqlf = '%s/gameServer/configdb_release.sql' % env.lpath


@task
@roles('sourceserver')
def pull_file():
    with settings(hide('warnings','stderr','stdout'),warn_only=True):
        local("mkdir -p %s/gameServer" % env.lpath)

        if parser.querysqls:
            with open(env.lpath + "/gameServer/gamedb_release.sql","w+") as f:
                f.write(parser.querysqls.replace(';',';\r\n'))
                logger.info("gamedb 获取完毕")

        if parser.dbname:
            local(parser.getdbdump())
            logger.info("configdb 获取完毕！")

        if parser.paths:
            for path in parser.paths.split(','):
                result = get(path.strip(), "%s/gameServer" % env.lpath)
                if result.failed and not("get file failed,Continue[Y/N]?"):
                    abort("Aborting file get task!")


def rsync_file(host):
    with settings(hide('warnings','stdout',),warn_only=True):
        with lcd(env.lpath):
            result = local('rsync -Pav gameServer -e "ssh -p %s" "%s":%s' %(env.port,host,env.lpath))

    if result.succeeded:
        logger.info("Push file to %s successful!" % host)
    else:
        logger.error("Push file to %s failed!" % env.host)

@task
@roles('%sgame' %parser.project)
@parallel(pool_size=5)
def push_file():
    execute(rsync_file,env.host)


@task
@roles('%sgame' %parser.project)
@parallel(pool_size=5)
def game_stop():
    with settings(hide('warnings','stderr','stdout'),warn_only=True):
        try:
            for java in java_u:
                if java.strip() in servers_java[env.host]:
                    result = run("set -m;sh /data/sh/switch/op/shutdown_game.sh %s >/dev/null &" % (java.strip()))
                    if result.succeeded:
                        logger.info("发送停止命令%s 上的%s游戏进程服 成功!" % (env.host,java))
                    else:
                        logger.error("发送停止命令%s 上的%s游戏进程服 失败!" %(env.host,java))
        except Exception as e:
            logger.error(str(e))

@task
@roles('%sgame' % parser.project)
@parallel(pool_size=5)
def game_check():
    with settings(hide('warnings','stdout','stderr',),warn_only=True):
        try:
            for java in java_u:
                if java.strip() in servers_java[env.host]:
                    result=run("ps -ef |grep -v grep |grep jar|grep -w %s" % java.strip())
                    if result.count(java) == 2:
                        print green("%s 游戏进程存活!" % java)
                    else:
                        print magenta("%s 游戏进程被杀死!" %java)
        except Exception as e:
            logger.error(str(e))

@task
@roles('%sgame' % parser.project)
@parallel(pool_size=5)
def update_server():
    with settings(hide('warnings','stdout','stderr',),warn_only=True):
        try:
            for java in java_u:
                if java.strip() in servers_java[env.host]:
                    if "cross"  in java:
                        if parser.c_config:
                            run("sed -i '%s' /app/warfare_cross/%s/config/game.properties" %(parser.c_config,java.strip()))
                            logger.info("%s配置文件修改成功" % java)

                        result1 = run("cp -rf %s/gameServer/warfare-cross.jar /app/warfare_cross/%s/" % (env.lpath,java.strip()))
                        result2 = run("rsync -avcz --update  %s/gameServer/*.jar --exclude=warfare-cross.jar /app/warfare_cross/%s/lib/" % (env.lpath,java.strip()))
                    else:
                        if parser.c_config:
                            run("sed -i '%s' /app/warfare/%s/gameServer/config/game.properties" %(parser.c_config,java.strip()))
                            logger.info("%s配置文件修改成功" % java)

                        result1 = run("rsync -avcz --update %s/gameServer/warfare-game.jar /app/warfare/%s/gameServer/" %(env.lpath,java.strip()))
                        result2 = run("rsync -avcz --update %s/gameServer/*.jar --exclude=warfare-game.jar /app/warfare/%s/gameServer/lib/" %(env.lpath,java.strip()))

                    if result1.succeeded and result2.succeeded:
                        logger.info("更新%s文件到 %s 成功!" % (java,env.host))
                    else:
                        print red("更新%s文件到 %s 失败!" %(java,env.host))
                        logger.error("更新%s文件到 %s 失败!" %(java,env.host))
        except Exception as e:
            logger.error(str(e))

@task
@roles('%sgame' % parser.project)
@parallel(pool_size=8)
def update_db():
    with settings(hide('warnings','stdout','stderr',),warn_only=True):
        try:
            for java in java_u:
                if java.strip() in servers_java[env.host]:
                    if parser.project == "cross":
                        configdb = "warfare_cross_config_" + java.split('_')[1].strip()
                        gamedb = "warfare_" + java.strip()

                        if parser.dbname:
                            result = run("/usr/local/db1/bin/mysql -h`awk -F[/:]+ '/db.config.url/{print $3}' /app/warfare_cross/%s/config/game.properties` -uwabao_game -p%s %s < %s" %(java.strip(),env.dbpassword,configdb,env.sqlf))
                            if result.succeeded:
                                logger.info("Update %s  %s 成功!" %(env.host, configdb))
                            else:
                                print red("Update %s %s 失败!" %(env.host, configdb))
                                logger.error("Update %s %s 失败!" %(env.host, configdb))

                        if parser.querysqls:
                            gamedbf = "%s/gameServer/gamedb_release.sql" % env.lpath
                            result = run("/usr/local/db1/bin/mysql -h`awk -F[/:]+ '/db.game.url/{print $3}' /app/warfare_cross/%s/config/game.properties` -uwabao_game -p%s %s -f < %s" %(java.strip(), env.dbpassword,gamedb,gamedbf))
                            if result.succeeded:
                                logger.info("Update %s %s 成功!" %(env.host, gamedb))
                            else:
                                print red("Update %s %s 失败!" %(env.host, gamedb))
                                logger.error("Update %s %s 失败!" %(env.host, gamedb))

                    if parser.project != "cross":
                        configdb = "configdb_" + java.strip()
                        gamedb = "gamedb_" + java.strip()
                        # sqlf = '/data/backup/database/wabao/%s/20170627/configdb_%s_db_datasql.sql' %(java.strip().split('_')[1],java.strip())
                        if parser.dbname:
                            result = run("/usr/local/db1/bin/mysql -h`awk -F[/:]+ '/db.config.url/{print $3}' /app/warfare/%s/gameServer/config/game.properties` -uwabao_game -p%s %s < %s" %(java.strip(),env.dbpassword,configdb,env.sqlf))
                            if result.succeeded:
                                logger.info("Update %s  %s 成功!" %(env.host, configdb))
                            else:
                                print red("Update %s %s 失败!" %(env.host, configdb))
                                logger.error("Update %s %s 失败!" %(env.host, configdb))

                        if parser.querysqls:
                            gamedbf = "%s/gameServer/gamedb_release.sql" % env.lpath
                            result = run("/usr/local/db1/bin/mysql -h`awk -F[/:]+ '/db.game.url/{print $3}' /app/warfare/%s/gameServer/config/game.properties` -uwabao_game -p%s %s -f < %s" %(java.strip(), env.dbpassword,gamedb,gamedbf))
                            if result.succeeded:
                                logger.info("Update %s %s 成功!" %(env.host, gamedb))
                            else:
                                print red("Update %s %s 失败!" %(env.host, gamedb))
                                logger.error("Update %s %s 失败!" %(env.host, gamedb))

        except Exception as e:
            logger.error(str(e))


@task
@roles('%sgame' %parser.project)
@parallel(pool_size=5)
def game_startup():
    with settings(hide('warnings','stdout','stderr',),warn_only=True):
        try:
            for java in java_u:
                if java.strip() in servers_java[env.host]:
                    result = run("set -m;sh /data/sh/switch/op/start_game.sh %s >/dev/null &" % java)
                    if result.succeeded:
                        logger.info("%s 上的%s游戏进程服开服命令发送 Success!" % (env.host,java))
                    else:
                        logger.error("%s 上的%s游戏进程服开服命令发送 Failed!" %(env.host,java))
        except Exception as e:
            logger.error(str(e))
