#!/usr/bin/env python 2.6.6
#-*- coding: utf-8 -*-

'''
Created on 2015-2-4

@author: 
'''

from abc import abstractmethod

class AbstractJob(object):

    @abstractmethod
    def create(self, args={}):
        raise NotImplementedError, "Cannot call abstract method"

    @abstractmethod
    def run(self, args={}):
        raise NotImplementedError, "Cannot call abstract method"

    @abstractmethod
    def stop(self, args={}):
        raise NotImplementedError, "Cannot call abstract method"

    @abstractmethod
    def destroy(self):
        raise NotImplementedError, "Cannot call abstract method"

