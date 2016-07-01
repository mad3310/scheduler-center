#!/usr/bin/env python
#-*- coding: utf-8 -*-

from handlers.http_request import HandlerRequestTask
from handlers.shell import HandlerShellTask

handlers = [
    (r"/task/request", HandlerRequestTask),
    (r"/task/shell", HandlerShellTask),
]