import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SmtpEmail(object):

    def __init__(self, host, from_addr, password):
        self.from_addr = from_addr
        self.server = smtplib.SMTP_SSL(host, 465)
        self.server.login(from_addr, password)

    def send_email(self, to_addrs, subject, content, atts=None):
        atts = atts or []
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = ','.join(to_addrs)
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        if atts:
            for att_name, att_content in atts:
                att_text = MIMEText(att_content, 'base64', 'utf-8')
                att_text["Content-Type"] = 'application/octet-stream'
                att_text["Content-Disposition"] = f'attachment; filename="{att_name}"'
                msg.attach(att_text)
        self.server.sendmail(self.from_addr, to_addrs, msg.as_string())
        self.server.close()
        return True


def main():
    email_host = 'smtp.qq.com'
    from_addr = ''  # 邮箱地址
    password = ''  # 授权码
    to_addrs = ['']  # 收件地址列表
    subject = 'python测试'
    content = 'python测试'
    attch_file = '/2019-04-20.xlsx'
    atts = [('asd.xlsx', open(attch_file, 'rb').read())]
    smtp_email = SmtpEmail(email_host, from_addr, password)
    smtp_email.send_email(to_addrs=to_addrs, subject=subject, content=content, atts=atts)


if __name__ == '__main__':
    main()

