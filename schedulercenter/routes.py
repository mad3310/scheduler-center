#!/usr/bin/env python
# encoding: utf-8

from handlers.http_request import HandlerTask

handlers = [
    (r"/task/", HandlerTask),
    (r"/task/(.*)", HandlerTask),
]