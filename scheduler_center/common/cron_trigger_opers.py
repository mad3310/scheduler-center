#!/usr/bin/env python 2.6.6
#coding:utf-8

import re

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from tornado.options import options

class TriggerOpers():
    """get trigger by args applied
    """

    def __init__(self, args={}):
        self.args = args
    
    def verify_params(self, args):
        pass
    
    def __get_cron_tgr_params(self):
        """
        
           m stand for month;
           d stand for day;
        """
        
        params_dict, result = {}, None
        month, day, week, day_of_week, hour, minute, second = None, None, None, None, None, None, None
        params = [month, day, week, day_of_week, hour, minute, second]
        params_dict = {'month':0, 'day':1, 'week':2, 'day_of_week':3, 'hour':4, 'minute':5, 'second':6}
        value = self.args.get('cron')
        
        num_unit_list = re.findall('(\d+)(\w+)', value)
        for num, unit in num_unit_list:
            index = params_dict[unit]
            params[index] = int(num)
        result = tuple(params)
        return result

    def __get_interval_tgr_params(self):
        params_dict, result = {}, None
        weeks, days, hours, minutes, seconds = 0, 0, 0, 0, 0
        params = [weeks, days, hours, minutes, seconds]
        value = self.args.get('interval')
        params_dict = {'days':0, 'weeks':1, 'hours':2, 'minutes':3, 'seconds':4}
        num, unit = re.findall('(\d+)(\w+)', value)[0]
        index = params_dict[unit]
        params[index] = int(num)
        result = tuple(params)
        return result

    def __get_date_tgr_params(self):
        return self.args.get('date')

    def get_cron_trigger(self):
        month, day, week, day_of_week, hour, minute, second = self.__get_cron_tgr_params()
        return CronTrigger(month=month, day=day, week=week, day_of_week=day_of_week, hour=hour, minute=minute, second=second)

    def get_intervel_trigger(self):
        weeks, days, hours, minutes, seconds = self.__get_interval_tgr_params()
        return IntervalTrigger(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)

    def get_date_trigger(self):
        run_date = self.__get_date_tgr_params()
        return DateTrigger(run_date=run_date)

    def get_trigger(self):
        """get trigger
        """
        
        TRIGGER_MAP = {
            'cron': self.get_cron_trigger,
            'interval': self.get_intervel_trigger,
            'date': self.get_date_trigger,
        }
        
        cron_k = list(set(self.args) & set(TRIGGER_MAP))[0]
        
        trigger_func = TRIGGER_MAP[cron_k]
        return trigger_func()

