import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown2
import json


with open("config.json", "r") as f:
    config = json.load(f)


# 发件人和收件人信息
sender_email = config["email"]["from"]
receiver_email = config["email"]["to"]
password = config["email"]["password"]

# 创建邮件内容
with open("README.md", "r") as f:
    body = f.read()
html_body = markdown2.markdown(body)

subject = "It's a test"

# 创建一个 MIMEMultipart 对象
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# 添加邮件正文
msg.attach(MIMEText(html_body, 'html'))

#
try:
    server = smtplib.SMTP_SSL(config["email"]["smtp_server"], config["email"]["smtp_port"])
    server.login(sender_email, password)  # 登录
    server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
    print("邮件发送成功！")
except Exception as e:
    print(f"邮件发送失败: {e}")
finally:
    server.quit()  # 关闭服务器连接

