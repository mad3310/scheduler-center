#!/usr/bin/env python
# encoding: utf-8

from handlers.http_request import HandlerRequestTask

handlers = [
    (r"/task/request", HandlerRequestTask),
]