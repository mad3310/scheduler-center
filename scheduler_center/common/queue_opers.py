#!/usr/bin/env python
#coding:gbk


from redis import Redis
from tornado.options import options
from utils.decorators import singleton

try:
    from rq import Queue
except ImportError:
    raise ImportError('rq module requires installed')


redis_con = None

#@singleton
class QueueOpers():
    
    def __init__(self, name):
        self.init_redis_con()
        #self.redis_con = Redis(host=options.redis_host, port=options.redis_port)
        self.queue = Queue(name=name, connection=self.redis_con)
    
    def init_redis_con(self):
        global redis_con
        if redis_con:
            self.redis_con = redis_con
        else:
            self.redis_con = Redis(host=options.redis_host, port=options.redis_port)
            redis_con = self.redis_con
        
    def enqueue(self, func, *args, **kwargs):
        job = self.queue.enqueue(f=func, args=args, kwargs=kwargs)
        return job


def enqueue(func, queue_name, *args, **kwargs):
    redis_conn = Redis(host=options.redis_host, port=options.redis_port)
    q = Queue(name=queue_name, connection=redis_conn)
    job = q.enqueue(func, *args, **kwargs)
    return job