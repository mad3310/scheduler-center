#!/usr/bin/env python
#-*- coding: utf-8 -*-


from redis import Redis
from tornado.options import options
from utils.decorators import singleton

try:
    from rq import Queue
except ImportError:
    raise ImportError('rq module requires installed')

def enqueue(queue_name, *args, **kwargs):
    redis_conn = Redis(host=options.redis_host, port=options.redis_port)
    q = Queue(name=queue_name, connection=redis_conn)

    kwargs.setdefault('ttl', 43)
    kwargs.setdefault('result_ttl', 10)

    job = q.enqueue('schedulerworker.job.job_opers.client_job_factory.client_job_run', *args, **kwargs)
    return job