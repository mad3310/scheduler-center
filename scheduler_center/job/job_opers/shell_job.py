#!/usr/bin/env python 2.6.6
#-*- coding: utf-8 -*-

'''
Created on 2015-2-4

@author: 
'''

from abstract_job import AbstractJob
from common.utils.invoke_command import InvokeCommand

class ShellJob(AbstractJob):
    
    def __init__(self, args={}):
        self.args = args
        self.create()
    
    def create(self, args={}):
        pass
    
    def run(self):
        shell_path = self.args.get('shell_path')
        iv = InvokeCommand()
        iv._runSysCmd(shell_path)