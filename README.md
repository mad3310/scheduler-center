# scheduler-center

## Introduction
定时任务中心
一般作为微服务体系中定时触发各服务得http和shell脚本类的任务。

## Build
在项目目录下执行，python setup.py bdist_rpm，执行操作后，可以看到在dist中产出三个rpm包，可以将noarch.rpm上传到yum源。每次版本更迭后，请注意修改版本号，版本号和release编号在setup.py文件中修改。
## Install and Deploy
通过yum的方式在需要部署的机器上进行安装。
在本地的安装中也可以使用yum命令，yum install schedulercenter-1.0.0-1.noarch.rpm
## Usage
* 启动：<br>
cd /usr/lib/python2.7/site-packages/ <br>
python schedulercenter/run.py &

* 关闭：<br>
找到相应的python进程，使用kill -5 {pid}

* 添加新的监控任务：<br>
curl "http://127.0.0.1:8000/task/" -X POST -d "url=http://scot.gome.inc/cb/api/execution/ping&interval=10seconds&priority=1&projectcode=test&taskname=baidutest&jobtype=httpRequestAccessInterface"<br>
url：待监控的url，返回结果有特定的格式要求<br>
interval：触发的频率<br>
priority：优先级，默认为1<br>
projectcode：业务线编码，指供应链内部各子系统的编码，比如：采购（purchase），需要大家后期统一商定，推荐都做一个5位的字母编码，提供一个编码表出来<br>
taskname：该项监控的名称<br>
jobtype：到sheduler-worker时的执行方式，默认为httpRequestAccessInterface，另外还提供httpRequest，shellRequest<br>

* 查看已有任务：<br>
curl "http://127.0.0.1:8000/task/"

* 删除任务：<br>
curl -X DELETE "http://127.0.0.1:8000/task/{task id}"<br>
task id指上述添加的任务id<br>
举例：curl -X DELETE "http://127.0.0.1:8000/task/8113b3a3210a41b49ce253a72ee9d86a"
## Change Log
### Add

### Change

### Fix

## More Infomation
启动服务后，需要执行一次任务查看动作，否则会影响定时任务的启动。
## TODO
* 添加任务中触发频率部分的多种模式的完善
* 添加任务中优先级的设定-加入紧急任务的添加
* jobtype中httpRequest，shellRequest，这两种操作方式的完善
* 优雅的关闭动作

## License
MIT
