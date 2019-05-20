#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging

from cron_trigger_opers import TriggerOpers
from scheduler_opers import SchedulerOpers
from queue_opers import enqueue
from tornado.options import options

class HttpRequestOpers():
    
    def add_http_job(self, params):
        
        job_dict = {}
        queue_name, url, cron = params
        cron_trigger_opers = TriggerOpers(cron)
        trigger = cron_trigger_opers.get_trigger()
        
        job_dict.setdefault('job_type', 'httpRequest')
        job_dict.setdefault('url', url)
        job_dict.setdefault('http_method', 'get')

        scheduler = SchedulerOpers(options.redis_jobstore, options.redis_runtime, options.redis_host, options.redis_port)
        scheduler.add_job(enqueue, trigger, queue_name, job_dict)