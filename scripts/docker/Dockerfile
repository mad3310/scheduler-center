FROM letv:centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm
RUN yum install scheduler-center -y
RUN yum install cronie -y
RUN yum update bash -y
RUN yum install tar -y
RUN yum install gbalancer -y
RUN yum install gbalancer-manager -y

EXPOSE 8888 9888
USER root

RUN mv /usr/lib64/python2.6/site-packages/SQLAlchemy-0.7.8-py2.6-linux-x86_64.egg/sqlalchemy /usr/lib64/python2.6/site-packages/

ENTRYPOINT service gbalancer-manager start && /bin/bash
