#!/usr/bin/env python 2.6.6
#-*- coding: utf-8 -*-

'''
Created on 2015-2-4

@author: 
'''

from abstract_job import AbstractJob
from common.utils.http_request import http_get


class HttpRequestJob(AbstractJob):
    
    def __init__(self, args={}):
        self.args = args
        self.create()
    
    def create(self):
        url = self.args.get('url')
        assert url
        self.url = url
    
    @staticmethod    
    def run(self):
        return http_get(self.url, _connect_timeout=60, _request_timeout=60)