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
#now = datetime.now().strftime('%Y-%m-%d')
now = "2017-04-10_16"
env.lpath = "/data/update_warfare/%s" % now

class Config:

	def __init__(self,cfile):
		self.cfile = cfile
		self.cfg = ConfigParser.ConfigParser()
		self.cfg.read(self.cfile)

		self.dbname = self.cfg.get('sql','dbname')
		self.ignore = self.cfg.get('sql','igtables')
		self.dbuser = 'wabao'
		self.dbpasswd = 'wabao*330?*@hero'
		#内网72的IP为125.88.171.116
		self.host = '125.88.171.116'
		self.tables = self.cfg.get('sql','table')

		self.querysqls = self.cfg.get('sql','querysql').split(';')
		self.querydb = self.cfg.get('sql','querysql')
	

		self.project = self.cfg.get('game','project')
		self.java_u = self.cfg.get('game','java_u')
		self.paths = self.cfg.get('game','paths')

	def getdbdump(self):
		if self.ignore.lower() == "yes":
			self.dbdump = "/usr/local/db1/bin/mysqldump -u%s -p%s -h%s %s --ignore-table=%s.activity_operation --ignore-table=%s.activity_notice --ignore-table=%s.cross_init --ignore-table=%s.activity_params >%s/gameServer/configdb_release.sql" % (self.dbuser,self.dbpasswd,self.host,self.dbname,self.dbname,self.dbname,self.dbname,self.dbname,env.lpath) 
			
		else:
			self.dbdump = ("/usr/local/db1/bin/mysqldump -u%s -p%s -h%s %s %s >%s/gameServer/configdb_release.sql") % (self.dbuser,self.dbpasswd,self.host,self.dbname,self.tables.split(','),env.lpath)
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

#carduser = {'fanti':['119.28.19.229'], 'jdfb':['114.55.11.191'],'cross':['114.55.11.191'],'en':['107.150.97.160']}
#servers_db 每台数据库分别存放了哪些游戏服的库
print red("config/%sserver_db.json" % parser.project)
servers_db = jsonload("config/%sserver_db.json" % parser.project)
#servers_java 每台服务器上分别存放了哪些游戏服
servers_java = jsonload("config/%sserver_info.json" %parser.project)
#归总所有的项目数据库密码
env.dbpassword = jsonload("config/sqlpasswd.json")[parser.project.strip()]
env.dbuser="wabao_game"

env.roledefs = {
	'sourceserver': ['root@125.88.171.116:9821'],
	#例如: 'fantigame': ['119.28.61.214'],
	parser.project + "game" : servers_java.keys(),
	#parser.project + "carduser" : carduser[parser.project]
}

#print red(servers_db)
#print yellow(servers_java)
print cyan(env.roledefs)

if parser.project in ['en','dw']:
	env.port = 36000
else:
	env.port = 22

env.user="root"
env.key_filename = "~/.ssh/jony"
env.password = "whosyourdaddy"
env.sqlf = '%s/gameServer/configdb_release.sql' % env.lpath

def update_sql(host,user,passwd,db,sqlf,port=3306):
	try:
		dbconn = MySQLdb.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
		#dbconn = MySQLdb.connect(host=host,port=port,user=user,passwd="warfareyf63wabaogame",db=db,charset='utf8')
		cur= dbconn.cursor()
		#sql=open(sqlf,'r').read()
		cur.execute('select now();')
		print cur.fetchall()
		#cur.execute(sql)
		logger.info('%s update Successful!' % db)
	except Exception, e:
		logger.error(str(e))
		#dbconn.rollback()
	finally:
		cur.close()
		dbconn.close()


@task
@roles('sourceserver')
def pull_file():
	with settings(hide('warnings','stderr','stdout'),warn_only=True):
		local("mkdir -p %s/gameServer" % env.lpath)
		local(parser.getdbdump())
		logger.info(parser.getdbdump())
		if parser.paths:
			for path in parser.paths.split(','):
				result = get(path.strip(), "%s/gameServer" % env.lpath)
			if result.failed and not("get file failed,Continue[Y/N]?"):
				abort("Aborting file get task!")


def rsync_file(host):
	with settings(hide('warnings','stdout',),warn_only=True):
		with lcd(env.lpath):
			print red(env.lpath)
			#result = put("gameServer/",'/tmp')
			#run("mkdir -p %s" %env.lpath)
			print yellow('rsync -Pav gameServer -e "ssh -p %s" "%s":%s' %(env.port,host,env.lpath))
			result = local('rsync -Pav gameServer -e "ssh -p %s" "%s":%s' %(env.port,host,env.lpath))
	if result.succeeded:
		logger.info("Push file to %s successful!" % host)
		print green("Push file to %s successful!" % host)
	else:
		logger.error("Push file to %s failed!" % env.host)
		print red("Push file to %s failed！" % host)

@task
@roles('%sgame' %parser.project)
@parallel(pool_size=5)		
def push_file():
	execute(rsync_file,env.host)


@task
@roles('%sgame' %parser.project)
@parallel(pool_size=5)
def game_stop():
	with settings(hide('warnings','stderr',),warn_only=True):
		try:
			for java in parser.java_u.split(','):
				if java.strip() in servers_java[env.host]:
					print green("set -m;sh /data/sh/switch/op/shutdown_game.sh %s >/dev/null &" % (java.strip()))
					result = run("sh /data/sh/switch/op/shutdown_game.sh %s" % (java.strip()))
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
						#此处如果更新文件里有lib/xxx.jar 可能也会直接放到
						print cyan("cp -rf %s/gameServer /app/warfare_cross/%s/" % (env.lpath,java.strip()))
						result = run("cp -rf %s/gameServer /app/warfare_cross/%s/" % (env.lpath,java.strip()))
					else:
						print green("cp -rf %s/gameServer /app/warfare/%s/" %(env.lpath,java.strip()))
						result = run("cp -rf %s/gameServer /app/warfare/%s/" %(env.lpath,java.strip()))
					if result.succeeded:
						logger.info("更新%s文件到 %s Success!" % (java,env.host))
					else:
						logger.error("更新%s文件到 %s Failed!" %(java,env.host))
		except Exception as e:
			logger.error(str(e))
							
		



@task
@roles("%sgame" % parser.project)
@parallel(pool_size=5)
def update_configdb():
	with settings(hide('stderr','stdout'),warn_only=True):
		print env.host
		try:
			for java in parser.java_u.split(','):
				env.sqlf = '%s/gameServer/configdb_release.sql' % env.lpath
				for host in servers_db:
					if java.strip() in servers_db[host]:	
						if parser.project == "cross":
							configdb = "warfare_cross_config_" + java.split('_').strip()[1]
						else:
							configdb = "configdb_" + java.strip()
						#update_sql(host,env.dbuser,env.dbpassword,db,env.sqlf)
						print magenta("mysql -h%s -uwabao_game -p%s %s -f < %s" %(host,env.dbpassword,configdb,env.sqlf))
						result = run("mysql -h%s -uwabao_game -p%s %s -e 'select version()'" %(host,env.dbpassword,configdb))
						if result.succeeded:
							logger.info("Update %s Configdb %s Successs!" %(host,db))
						else:
							logger.error("Update %s Configdb %s Failed!" %(host,db))
				continue	
		except Exception as e:
			print red(str(e))
			logger.error(str(e))


@task
@roles("%sgame" % parser.project)
@parallel(pool_size=5)
def update_gamedb():
	with settings(hide('stderr'),warn_only=True):
		print env.host
		try:
			for java in parser.java_u.split(','):
				env.sqlf = '%s/gameServer/gamedb_release.sql' % env.lpath
				for host in servers_db:
					if java.strip() in servers_db[host]:	
						if parser.project == "cross":
							db = "warfare_cross_" + java.split('_').strip()[1]
						else:
							db = "gamedb_" + java.strip()
						print green("%s,%s,%s,%s,%s" %(host,env.dbuser,env.dbpassword,db,env.sqlf))
						update_sql(host,env.dbuser,env.dbpassword,db,env.sqlf)
				continue	
		except Exception as e:
			print red(str(e))
			logger.error(str(e))


@task
@roles('%sgame' %parser.project)
@parallel(pool_size=5)
def game_startp():
	with settings(hide('warnings','stdout','stderr',),warn_only=True):
		try:
			for java in parser.java_u.split(','):
				if java.strip() in servers_java[env.host]:
					print green("set -m;sh /data/sh/switch/op/startgame.sh %s >/dev/null &" % java.strip())
					if "cross"  in java:
						#此处如果更新文件里有lib/xxx.jar 可能也会直接放到
						print green("rm -f /app/warfare_cross/%s/gameServer/*.release.sql" % java.strip())
						run("rm -f /app/warfare_cross/%s/gameServer/*.release.sql" % (java.strip()))
					else:
						print green("rm -f /app/warfare/%s/gameServer/*.release.sql" % java.strip())
						run("rm -f /app/warfare/%s/gameServer/*.release.sql" %(java.strip()))
					result = run("set -m;sh /data/sh/switch/op/startgame.sh %s >/dev/null &" % java.strip())
					if result.succeeded:
						logger.info("%s 上的%s游戏进程服开服命令发送 Success!" % (env.host,java))
					else:
						logger.error("%s 上的%s游戏进程服开服命令发送 Failed!" %(env.host,java))
		except Exception as e:
			logger.error(str(e))
