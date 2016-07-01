#!/usr/bin/env python 2.6.6
#coding:utf-8

import logging

from base import APIHandler

from tornado.options import options
from common.http_request_opers import HttpRequestOpers
from common.utils.exceptions import CommonException, HTTPAPIError


class HandlerRequestTask(APIHandler):
    
    http_request_opers = HttpRequestOpers()
    
    def __verify_params(self, args):
        """check params legality
        
           return is right and the right params
        """
        
        url = args.get('url')
        logging.info('get url:%s' % url)
        if not url:
            raise CommonException('url params are not supplied!')
        
        cron_set = set(['cron','interval','date']) & set(args)
        cron_key = cron_set.pop()
        logging.info('get cron key:%s' % cron_key)
        if not cron_key:
            logging.error('wrong here')
            raise CommonException('cron trigger params are not supplied!')
           
        cron_value = args.get(cron_key)
        cron = {cron_key:cron_value}
           
        queue_name = options.queue_http_request
        priority = args.get('priority')
        if priority and priority == '0':
            queue_name = options.queue_urgent
         
        params = (queue_name, url, cron)
        return params
    
    def post(self):
        """params include: url, 'cron' or 'interval' or 'date', priority 
        
        """
        
        args = self.get_all_arguments()
        print 'args: %s' % str(args)
        try:
            params = self.__verify_params(args)
        except Exception as err_msg:
            raise HTTPAPIError(status_code=400, error_detail=err_msg,\
                                notification = "direct", \
                                log_message= err_msg,\
                                response =  "please check params!")
        
        logging.info('get params:%s' % str(params) )
        self.http_request_opers.add_http_job(params)
        
        result = {}
        result.setdefault('message', 'add job in queue :%s successfully!' % options.queue_http_request)
        self.finish(result)
