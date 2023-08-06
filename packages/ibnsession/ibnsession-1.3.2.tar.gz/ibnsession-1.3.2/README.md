网络自动化运维工具
=======
该工具包含了网络设备一些基础操作，极大的简化了编程难度，对国产设备有着良好的支持。

目前支持的设备如下：

- 山石防火墙
- 华为路由交换设备
- 思科的asa防火墙，路由器

## 运行环境
```
[root@local ~]# cat /etc/redhat-release 
CentOS Linux release 7.2.1511 (Core) 

[root@szzabbixt01 ~]# python
Python 2.7.5 (default, Nov 20 2015, 02:00:19) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-4)] on linux2

[root@local ~]# pip show netmiko
Metadata-Version: 1.1
Name: netmiko
Version: 2.0.2
```


## 编程示例
```
ac_info = namedtuple('ac_info', ['username', 'password', 'enable_pass'])
ac_info.username = "username"
ac_info.password = "password"
ac_info.enable_pass = "en_pass"

dev_info = namedtuple('dev_info', ["dev_ip", "dev_name"])
dev_info.dev_ip = "192.168.0.1"

# 这里的 hs_SG6000 指的是所支持的山石防火墙的型号
# 目前支持 huawei_S5720 , asa_5545, srx_550 等等
dev_ob = hs_SG6000(ac_info,dev_info)

# 可以进行账号校验，判断账号是否登录成功且具有config权限
if dev_ob.account_verification():
    print("账号校验成功，具有CONFIG权限")

# 可以配置脚本
cmd_lines = []
cmd_lines.append('address "BCEL_185.22.9.97"')
cmd_lines.append('  ip 185.22.9.97/32')
cmd_lines.append('exit')

dev_ob.execute_script(cmd_lines):
```


## 版本记录
#### 1.3.2
- 优化了山石防火墙的账号校验部分
- 添加中文的介绍，以后会优先更新中文
- 添加了一个思科路由器的型号 cisco_C3900，把原本的 asa_5545 变成基类
- setup 的版本和这个保持同步



----

ibnsession
=======

Multi-vendor library to control network devices


## tool introducition
This tool is for ibn design


## Environment
```
[root@local ~]# cat /etc/redhat-release 
CentOS Linux release 7.2.1511 (Core) 

[root@szzabbixt01 ~]# python
Python 2.7.5 (default, Nov 20 2015, 02:00:19) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-4)] on linux2

[root@local ~]# pip show netmiko
Metadata-Version: 1.1
Name: netmiko
Version: 2.0.2
```

## Dir tree introduction
```
```


## Update log
#### 0.01 Design this package

#### 0.02 Add hillstone related update
- add function : generate_access_script(self,basic_info,session_list)
- add function : execute_access_script(self,access_script_list)

#### 0.1.0 Add SRX related update
- add function : generate_routing_script(self, route_info_list)
- add function : get_running_config(self)

#### 1.3 Add new module
- add huawei.py
- add cisco.py

#### 1.3.1 update huawei module
- remove print info
- update all module , add new parameter:config_mode_tag
```
account_verification(self, config_mode_tag="config"):
```