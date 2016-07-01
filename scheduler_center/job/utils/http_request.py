#!/usr/bin/env python 2.6.6
#-*- coding: utf-8 -*-

'''
Created on 2015-2-4

@author: 
'''

import logging
import json

from tornado.httpclient import HTTPRequest, HTTPError, HTTPClient


def request_fetch(request):
    """access to the target ip machine to retrieve the dict,then modify the config
    
    """
    
    http_client = HTTPClient()
    response = None
    try:
        response = http_client.fetch(request)
    except HTTPError, e:
        logging.error(e)
    
    return_result = False
    if response != None:    
        if response.error:
            return_result = False
            message = "remote access,the key:%s,error message:%s" % (request,response.error)
            logging.error(message)
        else:
            return_result = response.body.strip()
    http_client.close()
    return return_result

def http_get(url, _connect_timeout=40.0, _request_timeout=40.0, auth_username=None, auth_password=None):   
    try:
        request = HTTPRequest(url=url, method='GET', connect_timeout=_connect_timeout, request_timeout=_request_timeout,\
                              auth_username = auth_username, auth_password = auth_password)
        fetch_ret = request_fetch(request)
        return_dict = json.loads(fetch_ret)
        logging.info('GET result :%s' % str(return_dict))
        return return_dict
    except Exception, e:
        logging.error(str(e))
        return e