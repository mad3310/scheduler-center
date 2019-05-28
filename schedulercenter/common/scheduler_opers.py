#!/usr/bin/env python
#coding:utf-8

import time
import threading
import logging
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from tornado.options import options


class SchedulerOpers(object):

    # Global lock for creating global IOLoop instance
    _instance_lock = threading.Lock()
 
    def __init__(self, jobs_key=None, run_times_key=None, host=None, port=None):
        jobstores = {
            'default': RedisJobStore(jobs_key=jobs_key, run_times_key=run_times_key, host=host, port=port)
        }
        executors = {
            'default': {'type': 'threadpool', 'max_workers': 20},
            'processpool': ProcessPoolExecutor(max_workers=5)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self._scheduler = TornadoScheduler()
        self._scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
        self._scheduler.start()
 
    def add_job(self, func, trigger, *args, **kwargs):

        project_code = kwargs.get('project_code')
        task_name = kwargs.get('task_name')
        job_name = "%s-%s" % (project_code, task_name)

        self._scheduler.add_job(func, trigger, args=args, kwargs=kwargs, name=job_name)


    def start(self):
        self._scheduler.start()

    def get_all_job(self):
        jobs = self._scheduler.get_jobs()
        if jobs:
            for job in jobs:
                print(u'    %s' % job)


        return jobs

    def remove_job(self, job_id):
        self._scheduler.remove_job(job_id)

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

