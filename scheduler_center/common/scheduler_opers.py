#!/usr/bin/env python 2.6.6
#coding:utf-8

import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from tornado.options import options
from utils.decorators import singleton


#background_scheduler = BackgroundScheduler()


# class SchedulerOpers():
#     
#     def __init__(self, jobs_key, run_times_key, host, port):
#         self.background_scheduler = BackgroundScheduler()
#         self.redis_jobstore = RedisJobStore(jobs_key=options.redis_jobstore, run_times_key=options.redis_runtime, 
#                                             host=options.redis_host, port=options.redis_port)
#         self.background_scheduler.add_jobstore(self.redis_jobstore)
# 
# #         global background_scheduler
# #         if background_scheduler:
# #             #logging.info('')
# #             self.background_scheduler = background_scheduler
# #         else:
# #             self.background_scheduler = BackgroundScheduler()
# #             background_scheduler = self.background_scheduler
# 
#     def add_jobstore(self):
#         self.background_scheduler.add_jobstore(self.redis_jobstore)
#     
#     def add_job(self, func, trigger, *args, **kwargs):
#         #self.add_jobstore()
#         self.background_scheduler.add_job(func, trigger, args=args, kwargs=kwargs)
#         self.background_scheduler.start()
#     
#     def start(self):
#         self.background_scheduler.start()


def start_scheduler_server():
    scheduler_opers_obj = SchedulerOpers(options.redis_jobstore, options.redis_runtime,\
                                         options.redis_host, options.redis_port)
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
 
    def start(self):
        self._scheduler.start()

