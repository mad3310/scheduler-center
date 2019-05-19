#!/usr/bin/env python
# encoding: utf-8

import os

from tornado.options import define

join = os.path.join
dirname = os.path.dirname

base_dir = os.path.abspath(dirname(dirname(dirname(__file__))))

define("base_dir", default=base_dir, help="project base dir")
define('debug', default=False, type=bool, help='is debuging?')
define('port', default=8000, type=int, help='app listen port')

define('send_email_switch', default=True, type=bool, help='the flag of if send error email')
define('admins', default=("zhoubingzheng <zhoubingzheng@letv.com>", ), help='admin email address')
define('smtp_host', default="mail.letv.com", help='smtp host')
define('smtp_port', default=587, help='smtp port')
define('smtp_user', default="mcluster", help='smtp user')
define('smtp_password', default="Mcl_20140903!", help = 'smtp password')
define('smtp_from_address', default='mcluster@letv.com', help='smtp from address')
define('smtp_duration', default=10000, type=int, help='smtp duration')
define('smtp_tls', default=False, type=bool, help='smtp tls')

define("redis_host", default="127.0.0.1", help="redis host to login")
define("redis_port", default=6379, help="redis host to port")
define("redis_jobstore", default="djj", help="name of redis jobstroe")
define("redis_runtime", default='dj', help="name of redis runtime")

define("queue_urgent", default="webportal_urgent", help="redis queue to store urgent job")
define("queue_http_request", default="webportal_get", help="redis queue to store get request job")
define("queue_shell", default="webportal_shell", help="redis queue to store run shell job")