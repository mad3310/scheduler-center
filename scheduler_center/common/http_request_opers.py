#!/usr/bin/env python 2.6.6
#coding:utf-8

import logging
import scheduler_opers

from cron_trigger_opers import TriggerOpers
from scheduler_opers import SchedulerOpers
from queue_opers import QueueOpers, enqueue
from job.job_opers.run_job import run_script
from tornado.options import options

class HttpRequestOpers():
    
    def add_http_job(self, params):
        
        #global scheduler_opers_obj
        
        get_job_dict = {}
        queue_name, url, cron = params
        cron_trigger_opers = TriggerOpers(cron)
        trigger = cron_trigger_opers.get_trigger()
        
        get_job_dict.setdefault('url', url)
        
        #queue_opers = QueueOpers(queue_name)
        scheduler = SchedulerOpers(options.redis_jobstore, options.redis_runtime, options.redis_host, options.redis_port)

        #scheduler.add_job(enqueue, trigger, HttpRequestJob(get_job_dict).run, queue_name)
        scheduler.add_job(enqueue, trigger, run_script, queue_name, get_job_dict)