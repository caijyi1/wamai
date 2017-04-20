#!/usr/bin/env python
#-*- coding:utf8 -*-

from datetime import datetime
import MySQLdb
import json
from fabric.colors import *
import os,logging,sys,json
import logging.handlers
import subprocess
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
		self.querydb = self.cfg.get('gamedb_sql','querydb')
	

		self.project = self.cfg.get('game','project')
		self.java_u = self.cfg.get('game','java_u').replace("\"","")
		self.paths = self.cfg.get('game','paths')
		self.c_config = self.cfg.get('game','c_config')

	def getdbdump(self):
		if self.ignore.lower() == "yes":
			self.dbdump = "/usr/local/db1/bin/mysqldump -u%s -p%s -h%s %s --ignore-table=%s.activity_operation --ignore-table=%s.activity_notice --ignore-table=%s.cross_init --ignore-table=%s.activity_params >%s/gameServer/configdb_release.sql" % (self.dbuser,self.dbpasswd,self.host,self.dbname,self.dbname,self.dbname,self.dbname,self.dbname,env.lpath) 
		else:
			self.dbdump = ("/usr/local/db1/bin/mysqldump -u%s -p%s -h%s %s %s >%s/gameServer/configdb_release.sql") % (self.dbuser,self.dbpasswd,self.host,self.dbname,self.tables.replace(","," "),env.lpath)
		return self.dbdump
	

def initLoggerWithRotate():
	current_time = datetime.now().strftime("%Y%m%d")
	logpath = "/tmp"
	logfile = "fabfile_" + current_time + ".log"
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
parser=Config(CFILE)

def jsonload(f):
	with open(f,'r') as json_file:
		data=json.load(json_file)
		return data

carduser = {'fanti':['120.28.19.229'], 'jdfb':['114.55.11.191'],'cross':['114.55.11.191'],'en':['107.150.97.160'],'dw':['35.156.104.76']}
#servers_db 每台数据库分别存放了哪些游戏服的库
servers_db = jsonload("config/%sserver_db.json" % parser.project)
#servers_java 每台服务器上分别存放了哪些游戏服
servers_java = jsonload("config/%sserver_info.json" %parser.project)
#归总所有的项目数据库密码
env.dbpassword = jsonload("config/sqlpasswd.json")[parser.project.strip()]
env.dbuser="wabao_game"
env.lpath = "/data/update_warfare/%s_%s" %(parser.actime,parser.project)

env.roledefs = {
	'sourceserver': ['root@125.88.171.116:9821'],
	'jumpser': list(carduser[parser.project]),
	#例如: 'fantigame': ['119.28.61.214'],
	parser.project + "game" : servers_java.keys(),
}

print cyan(env.roledefs)
print magenta(parser.java_u)
print magenta(parser.paths)

if parser.project in ['en','dw']:
	env.port = 36000
else:
	env.port = 22

env.user="root"
env.sqlf = '%s/gameServer/configdb_release.sql' % env.lpath


@task
@roles('sourceserver')
def pull_file():
	with settings(hide('warnings','stderr','stdout'),warn_only=True):
		local("mkdir -p %s/gameServer" % env.lpath)
		if parser.querysqls:
			with open(env.lpath + "/gameServer/gamedb_release.sql","w+") as f:
				f.write(parser.querysqls)
		local(parser.getdbdump())
		logger.info("sql 获取完毕！")
		if parser.paths:
			for path in parser.paths.split(','):
				print red(path.strip())
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
			for java in parser.java_u.split(','):
				if java.strip() in servers_java[env.host]:
					print green("set -m;sh /data/sh/switch/op/shutdown_game.sh %s >/dev/null &" % (java.strip()))
					result = run("set -m;sh /data/sh/switch/op/shutdown_game.sh %s >/dev/null &" % (java.strip()))
					if result.succeeded:
						logger.info("发送停止命令%s 上的%s游戏进程服 Success!" % (env.host,java))
					else:
						logger.error("发送停止命令%s 上的%s游戏进程服 Failed!" %(env.host,java))
		except Exception as e:
			logger.error(str(e))

@task
@roles('%sgame' % parser.project)
@parallel(pool_size=5)
def game_check():
	with settings(hide('warnings','stdout','stderr',),warn_only=True):
		try:
			for java in parser.java_u.split(','):
				if java.strip() in servers_java[env.host]:
					result=run("ps aux |grep -v grep|grep %s" %java.strip())
					if result.count(java.strip()) == 2:
						print blue("%s 游戏进程存活!" % java)
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
			for java in parser.java_u.split(','):
				if java.strip() in servers_java[env.host]:
					if "cross"  in java:
						if parser.c_config:
							print cyan("配置文件将进行修改...")
							run("sed -i '%s' /app/warfare_cross/%s/config/game.properties" %(parser.c_config,java.strip()))
							logger.info("%s配置文件修改成功" % java)
						#此处如果更新文件里有lib/xxx.jar 可能也会直接放到
						print cyan("%s服正在更新..." % java.strip())
						result1 = run("cp -rf %s/gameServer/warfare-cross.jar /app/warfare_cross/%s/" % (env.lpath,java.strip()))
						result2 = run("rsync -avcz --update  %s/gameServer/*.jar --exclude=warfare-cross.jar /app/warfare_cross/%s/lib/" % (env.lpath,java.strip()))
					else:
						if parser.c_config:
							run("sed -i '%s' /app/warfare/%s/gameServer/config/game.properties" %(parser.c_config,java.strip()))
							logger.info("%s配置文件修改成功" % java)
						print green("%s 服正在更新" % java)
						result1 = run("rsync -avcz --update -n %s/gameServer/warfare-game.jar /app/warfare/%s/gameServer/" %(env.lpath,java.strip()))
						result2 = run("rsync -avcz --update -n %s/gameServer/*.jar --exclude=warfare-game.jar /app/warfare/%s/gameServer/lib/" %(env.lpath,java.strip()))
					if result1.succeeded and result2.succeeded:
						logger.info("更新%s文件到 %s Success!" % (java,env.host))
					else:
						logger.error("更新%s文件到 %s Failed!" %(java,env.host))
		except Exception as e:
			logger.error(str(e))
							
		



@task
@roles('jumpser')
@parallel(pool_size=5)
def update_db():
	with settings(hide('stderr','warnings','stdout'),warn_only=True):
		try:
			for java in parser.java_u.split(','):
				configdbf = '%s/gameServer/configdb_release.sql' % env.lpath
				for host in servers_db:
					if java.strip() in servers_db[host]:	
						if parser.project == "cross":
							configdb = "warfare_cross_config_" + java.split('_')[1].strip()
							gamedb = "warfare_cross_" + java.split('_')[1].strip()
						else:
							configdb = "configdb_" + java.strip()
							gamedb = "gamedb_" + java.strip()
						result = run("/usr/local/db1/bin/mysql -h%s -uwabao_game -p%s %s -f < %s " %(host, env.dbpassword, configdb, env.sqlf))
						if result.succeeded:
							logger.info("Update %s  %s Successs!" %(host, configdb))
						else:
							logger.error("Update %s %s Failed!" %(host, configdb))
						if parser.querysqls:
							gamedbf = "%s/gameServer/gamedb_release.sql" % env.lpath
							print magenta("/usr/local/db1/bin/mysql -h%s -uwabao_game -p%s %s -f < %s" %(host, env.dbpassword, gamedb,gamedbf))
							result = run("/usr/local/db1/bin/mysql -h%s -uwabao_game -p%s %s -f < %s" %(host, env.dbpassword,gamedb,gamedbf))
							if result.succeeded:
								logger.info("Update %s %s Successs!" %(host, gamedb))
							else:
								logger.error("Update %s %s Failed!" %(host, gamedb))
				continue	
		except Exception as e:
			print red(str(e))
			logger.error(str(e))

@task
@roles('%sgame' %parser.project)
@parallel(pool_size=5)
def game_startup():
	with settings(hide('warnings','stdout','stderr',),warn_only=True):
		try:
			for java in parser.java_u.split(','):
				if java.strip() in servers_java[env.host]:
					result = run("set -m;sh /data/sh/switch/op/start_game.sh %s >/dev/null &" % java.strip())
					if result.succeeded:
						logger.info("%s 上的%s游戏进程服开服命令发送 Success!" % (env.host,java))
					else:
						logger.error("%s 上的%s游戏进程服开服命令发送 Failed!" %(env.host,java))
		except Exception as e:
			logger.error(str(e))
