由于电池测试所连主机有线网口被占用，故只能采用无线连接的方式，但是目前无线连接稳定性较差，虽然有配置[固定ip的方法](https://blog.csdn.net/weixin_42442847/article/details/91420359)，但其鲁棒性未知。

example_cc98.ps1是一个自动获取校内IP并发送到浙大邮箱的powershell脚本，但是脚本能够被直接打开，邮箱、密码容易泄露。虽然也有将powershell脚本转为exe的方法，但是powershell只能在windows设备上运行，再者，powershell可扩展性不如python，故有此使用python实现的项目。

使用浙大邮箱是因为，不需要认证，不需要连接外网就能使用。

# 使用方法
1. 创建config.json文件，填入如下信息：

```json
{
    "mail_host": "smtp.zju.edu.cn",
    "mail_user": ZJU邮箱用户名，学号或者别名，不包括“@zju.edu.cn”,
    "mail_pass": ZJU邮箱密码,
    "sender": 发送邮箱（上面的用户名+@zju.edu.cn）,
    "receivers": [接收邮箱列表],
    "period": 30
}
```

2. 运行IPMonitor\.py

Windows平台可以使用 pyinstaller.exe –F IPMonitor\.py 命令打包成exe文件并放进计划任务开机自启