#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess

class InvokeCommand():
    
    def _runSysCmd(self,cmdStr):
        if cmdStr == "":
            return ("",0)
        p = subprocess.Popen(cmdStr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ret_str = p.stdout.read()
        retval = p.wait()
        return (ret_str,retval)

    def _runSysCmdnoWait(self,cmdStr):
        if cmdStr == "":
            return False
        try:
            p = subprocess.Popen(cmdStr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception, e:
            return False
        if p.poll():
            return False
        else:
            return p