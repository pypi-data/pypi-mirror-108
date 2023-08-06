#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
service_path = os.getenv('SERVICE_PATH')
# port = os.getenv('PORT')
# worker_num = os.getenv('WORKER_NUM')
# request_timeout = os.getenv('REQUEST_TIMEOUT')
# bind = '0.0.0.0:5000'      #绑定ip和端口号
# if port:
#     bind = '0.0.0.0:'+port      #绑定ip和端口号
# backlog = 512                #监听队列
#
# timeout = 60      #超时
# if request_timeout:
#     timeout = request_timeout      #超时
# worker_class = 'gevent' #使用gevent模式，还可以使用sync 模式，默认的是sync模式
# # workers = multiprocessing.cpu_count() * 2 + 1    #进程数
# workers = 1    #进程数
# if worker_num:
#     workers = worker_num    #进程数
#
# threads = 2    #指定每个进程开启的线程数
# loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# if not service_path:
#     service_path = '.'
pidfile = service_path+"/logs/gunicorn.pid"        #错误日志文件
accesslog = service_path+"/logs/access.log"      #访问日志文件
errorlog = service_path+"/logs/error.log"        #错误日志文件