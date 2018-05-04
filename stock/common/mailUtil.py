import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import pandas as pd
from common import constant as con

def sendEmail(title,msg):
    # 发送邮件服务器
    smtpserver = 'smtp.163.com'
    # 发送邮箱用户名和密码
    user = 'wtwtawt@163.com'
    password = 'wtwtawt23'
    # 发送邮箱
    sender = 'wtwtawt@163.com'
    # 接受邮箱
    receiver = list(pd.read_csv(con.memberPath + 'member.csv', encoding='gbk').email)
    # receiver = 'wtwtawt@163.com'

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = 'wtwtawt@163.com'
    # message['To'] = '276424131@qq.com'
    message['Subject'] = Header(title, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText(msg, 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的test.txt文件
    # att1 = MIMEText(open('123.txt', 'rb').read(), 'base64', 'utf-8')
    # att1['Content-Type'] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字 邮件中就显示什么名字
    # att1['Content-Disposition'] = 'attachment;filename:"123.txt"'
    # message.attach(att1)

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, message.as_string())
    smtp.quit()