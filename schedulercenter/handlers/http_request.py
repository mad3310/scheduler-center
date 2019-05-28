#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging

from base import APIHandler
from tornado.options import options
from schedulercenter.common.utils.exceptions import CommonException, HTTPAPIError
from schedulercenter.common.scheduler_opers import SchedulerOpers
from schedulercenter.common.cron_trigger_opers import TriggerOpers
from schedulercenter.common.queue_opers import enqueue


class HandlerTask(APIHandler):

    def __verify_params(self, args):
        """check params legality
        
           return is right and the right params
        """
        
        url = args.get('url')
        logging.info('get url of post param: %s' % url)
        if not url:
            raise CommonException('url params are not supplied!')
        
        cron_set = set(['cron','interval','date']) & set(args)
        cron_key = cron_set.pop()
        logging.info('get cron key:%s' % cron_key)
        if not cron_key:
            raise CommonException('cron trigger params are not supplied!')

        project_code = args.get('projectcode')
        if not project_code:
            raise CommonException('project code should be specify!')

        task_name = args.get('taskname')
        if not task_name:
            raise CommonException('task name should be specify!')

        job_type = args.get('jobtype')
        if not job_type:
            raise CommonException('job type should be specify!')
           
        cron_value = args.get(cron_key)
        cron = {cron_key:cron_value}
           
        queue_name = options.queue_http_request
        priority = args.get('priority')
        if priority and priority == '0':
            queue_name = options.queue_urgent
         
        params = (queue_name, job_type, url, cron, project_code, task_name)
        return params

    def __add_http_job(self, params):

        queue_name, job_type, url, cron, project_code, task_name = params
        cron_trigger_opers = TriggerOpers(cron)
        trigger = cron_trigger_opers.get_trigger()

        SchedulerOpers.instance().add_job(enqueue,
                                          trigger,
                                          job_type=job_type,
                                          url=url,
                                          http_method='get',
                                          project_code=project_code,
                                          task_name=task_name,
                                          queue_name=queue_name)
    
    def post(self):
        """params include: url, 'cron' or 'interval' or 'date', priority

            call example:
               curl "http://127.0.0.1:8000/task/" -X POST -d "url=http://scot.gome.inc/cb/api/execution/ping&interval=10seconds&priority=1&projectcode=test&taskname=baidutest&jobtype=httpRequestAccessInterface"
        
        """
        
        args = self.get_all_arguments()
        logging.info(u'args: %s' % args)
        try:
            params = self.__verify_params(args)
        except Exception as err_msg:
            raise HTTPAPIError(status_code=400, error_detail=err_msg, \
                                notification = "direct", \
                                log_message= err_msg, \
                                response = "please check params!")
        
        logging.info('get params:%s' % str(params))
        self.__add_http_job(params)
        
        result = {}
        result.setdefault('message', 'add job in queue :%s successfully!' % options.queue_http_request)
        self.finish(result)


    def get(self):
        """
        retrieve all secheduler jobs

        call example:
            curl "http://127.0.0.1:8000/task/"

        :return:
        """
        jobs = SchedulerOpers.instance().get_all_job()

        message = 'list the scheduler all jobs detail: %s' % jobs
        if jobs == []:
            message = 'No job! You can add a job!'

        result = {}
        result.setdefault('message', message)
        self.finish(result)

    def delete(self, *args, **kwargs):
        """
        delete specify the job

        call example:
            curl -X DELETE "http://127.0.0.1:8000/task/8113b3a3210a41b49ce253a72ee9d86a"

            8113b3a3210a41b49ce253a72ee9d86a is a example of job id, you can pass the real job id on the rquest.
        :param args:
        :param kwargs:
        :return:
        """
        if args is ():
            raise HTTPAPIError(status_code=400,
                               error_detail='For delete job, you should be specify a valid job id.', \
                               notification="direct", \
                               log_message='For delete job, you should be specify a valid job id.', \
                               response="please specify a valid job id! append the job id after task/.")
        job_id = args[0]
        if job_id == None:
            raise HTTPAPIError(status_code=400, error_detail='please specify the job id param for delete the job operations!', \
                               notification="direct", \
                               log_message='For delete job operation, need to be specify the job id', \
                               response="please check params!")

        jobs = SchedulerOpers.instance().get_all_job()

        job_id_array = []
        for job in jobs:
            job_id_array.append(job.id)

        if jobs is None or not job_id in job_id_array:
            raise HTTPAPIError(status_code=400,
                               error_detail='pass the job id not exist!', \
                               notification="direct", \
                               log_message='pass the job id not exist!', \
                               response="please specify a valid job id!")


        SchedulerOpers.instance().remove_job(job_id)

        result = {}
        result.setdefault('message', 'job[%s] has been deleted!' % (job_id))
        self.finish(result)

