#!/usr/bin/env python 2.6.6
#coding:utf-8

import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from tornado.options import options
from utils.decorators import singleton


def start_scheduler_server():
    scheduler_opers_obj = SchedulerOpers(options.redis_jobstore, options.redis_runtime, options.redis_host, options.redis_port)
    scheduler_opers_obj.start()


@singleton
class SchedulerOpers(object):
 
    def __init__(self, jobs_key, run_times_key, host, port):
        self._scheduler = BackgroundScheduler()
        self.redis_js = RedisJobStore(jobs_key=jobs_key, run_times_key=run_times_key, host=host, port=port)
        self._scheduler.add_jobstore(self.redis_js)
 
    def add_jobstore(self):
        self._scheduler.add_jobstore(self.redis_js)
 
    def add_job(self, func, trigger, *args, **kwargs):
        self._scheduler.add_job(func, trigger, args=args, kwargs=kwargs)
        self._scheduler.start()

    def start(self):
        self._scheduler.start()

