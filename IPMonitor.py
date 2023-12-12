import socket
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json
import time
import datetime
import threading

class IPMonitor:
    # 可以直接在__init__中初始化，启动，不需要另外来个函数
    def __init__(self):
        with open("config.json", 'r', encoding="utf-8") as f:
            config = json.load(f)
    
        self.mail_host = config["mail_host"]
        self.mail_user = config["mail_user"]
        self.mail_pass = config["mail_pass"]
        self.sender = config["sender"]
        self.receivers = config["receivers"]
        self.period = config["period"]# 获取ip周期，单位：秒
        self.last_ip_address = None

        self.timer = threading.Timer(1, self.func_timer)
        self.timer.start()
    
    def send_mail(self, content):
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header("IPMonitor")
        message['To'] =  Header(self.mail_user)
        
        subject = 'IPMonitor'
        message['Subject'] = Header(subject, 'utf-8')
        
        
        try:
            smtpObj = smtplib.SMTP() 
            smtpObj.connect(self.mail_host, 25)    # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass)  
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print("Sent successfully")
        except smtplib.SMTPException:
            print("Failed to send")
    
    def get_host_ip(self):
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip

    def func_timer(self):        
        self.func_task()

        # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
        self.timer = threading.Timer(self.period, self.func_timer)   # 每过一段随机时间（单位：秒）调用一次函数
        self.timer.start()    #启用定时器
    
    def func_task(self):
        ip_address = self.get_host_ip()
        time_now = str(datetime.datetime.now())
        print(time_now + ' ' + ip_address)
        if(ip_address != self.last_ip_address):
            self.last_ip_address = ip_address
            self.send_mail(ip_address)

if __name__ == "__main__":
    ip_monitor = IPMonitor()
    
    