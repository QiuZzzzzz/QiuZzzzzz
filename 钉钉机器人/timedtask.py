


from interval import Interval
 
from datetime import date, datetime

import time
from apscheduler.schedulers.blocking import BlockingScheduler
import configparser
import os
import sys
from subprocess import Popen, PIPE, STDOUT
import test1


def func():
    import datetime
    import robot220414
    
    config = configparser.ConfigParser()
    filename = 'mypy.ini'
    config.read(filename, encoding='utf-8')
    #config.read(open('mypy.ini'))

    noon=config.get("H5","noon")
    evening=config.get("H5","evening")
    statistic1=config.get("H5","statistic1")
    statistic2=config.get("H5","statistic2")
    now = datetime.datetime.now()
    ts = str(now.strftime('%Y-%m-%d %H:%M'+':00'))
    ts2 = str(now.strftime('%Y-%m-%d'))
    start_time = str(datetime.datetime.strptime(str(datetime.datetime.now().date()) + '08:30', '%Y-%m-%d%H:%M'))
    end_time = str(datetime.datetime.strptime(str(datetime.datetime.now().date()) + '14:00', '%Y-%m-%d%H:%M'))
    statistic_time1=str(datetime.datetime.strptime(str(datetime.datetime.now().date()) + '10:50', '%Y-%m-%d%H:%M'))
    statistic_time2=str(datetime.datetime.strptime(str(datetime.datetime.now().date()) + '16:30', '%Y-%m-%d%H:%M'))
    if start_time<=ts and noon!=ts2:
       config.set("H5","noon", ts2)
       config.write(open(filename, 'w'))
       #robot220414.send_md_msg()
       #p = Popen([sys.executable, "robot220414.py"],stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    if end_time<=ts and evening!=ts2:
        config.set("H5","evening", ts2)
        config.write(open(filename, 'w'))
        #robot220414.send_md_msg()
        #p = Popen([sys.executable, "robot220414.py"],stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    if statistic_time1<=ts and statistic1!=ts2:
        config.set("H5","statistic1", ts2)
        config.write(open(filename, 'w'))
        print('1')
        print(test1.aa())
        #robot220414.send_statistic()
    if statistic_time2<=ts and statistic2!=ts2:
        config.set("H5","statistic2", ts2)
        config.write(open(filename, 'w'))
       # robot220414.send_statistic()

    

    
def dojob():
    import datetime
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    now = datetime.datetime.now()
    #添加任务,时间间隔2S
    scheduler.add_job(func, 'interval', seconds=10)
    #添加任务,时间间隔5S

    scheduler.start()
dojob()

