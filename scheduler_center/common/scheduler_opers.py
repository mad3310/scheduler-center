#!/usr/bin/env python
#coding:utf-8

import time
import threading
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.redis import RedisJobStore
from tornado.options import options


class SchedulerOpers(object):

    # Global lock for creating global IOLoop instance
    _instance_lock = threading.Lock()
 
    def __init__(self, jobs_key=None, run_times_key=None, host=None, port=None):
         self._scheduler = TornadoScheduler()
         self.redis_js = RedisJobStore(jobs_key=jobs_key, run_times_key=run_times_key, host=host, port=port)
         self._scheduler.add_jobstore(self.redis_js)
         logging.info('scheduler server starts')
         self._scheduler.start()
 
    def add_job(self, func, trigger, *args, **kwargs):
        print(self._scheduler)
        self._scheduler.add_job(func, trigger, args=args, kwargs=kwargs)


    def start(self):
        self._scheduler.start()
        print(self._scheduler)
        print(self._scheduler.running)

    def get_all_job(self):
        jobs = self._scheduler.get_jobs(self.redis_js)
        print self._scheduler
        print self._scheduler.print_jobs(self.redis_js)
        print self._scheduler.running
        return jobs

    @staticmethod
    def instance():
        """Returns a global `IOLoop` instance.
        Most applications have a single, global `IOLoop` running on the
        main thread.  Use this method to get this instance from
        another thread.  In most other cases, it is better to use `current()`
        to get the current thread's `IOLoop`.
        """
        if not hasattr(SchedulerOpers, "_instance"):
            with SchedulerOpers._instance_lock:
                if not hasattr(SchedulerOpers, "_instance"):
                    # New instance after double check
                    SchedulerOpers._instance = SchedulerOpers(options.redis_jobstore,
                                          options.redis_runtime_key,
                                          options.redis_host,
                                          options.redis_port)
        return SchedulerOpers._instance

