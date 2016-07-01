#!/usr/bin/env python 2.6.6
#coding:utf-8

import logging

from base import APIHandler
from common.cron_trigger import TriggerOpers
from common.queue_opers import QueueOpers
from job.job_opers.http_request_job import HttpRequestJob
from tornado.options import options

class HandlerShellTask(APIHandler):

    def __verify_params(self, args):
        result = True
        queue_name = options.queue_shell
        shell_path = args.get('shell_path')
        cron_k = 'cron' or 'interval' or 'date' in args
        cron_v = args.get(cron_k)
        priority = args.get('priority')
        if priority and priority == '0':
            queue_name = options.queue_urgent
        logging.info('get shell_path:%s' % shell_path)
        logging.info('get cron :%s, value:%s' % (cron_k, cron_v) )
        if not (shell_path and cron_k and cron_v):
            result = False
        params = (queue_name, shell_path, cron_k, cron_v)
        return result, params
    
    def post(self):
        
        get_job_dict, cron_dict = {}, {}
        
        args = self.get_all_arguments()
        result, params =  self.__verify_params(args)
        if not self.__verify_params(args):
            raise HTTPAPIError(status_code=400, error_detail="params are not enough!",\
                                notification = "direct", \
                                log_message= "params are not enough!",\
                                response =  "please check params!")
        
        queue_name, shell_path, cron_k, cron_v = params
        cron_dict.setdefault(cron_k, cron_v)
        cron_trigger_opers = TriggerOpers(cron_dict)
        trigger = cron_trigger_opers.get_trigger()
        
        get_job_dict.setdefault('shell_path', shell_path)
        get_job = HttpRequestJob(get_job_dict)
        
        queue_opers = QueueOpers(queue_name)
        scheduler.add_job(queue_opers.enqueue, trigger, get_job.run)
        
        result = {}
        result.setdefault('message', 'add shell job in queue: %s' % options.queue_shell)
        self.finish(result)
