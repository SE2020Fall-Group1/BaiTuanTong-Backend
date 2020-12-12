import smtplib
from email.mime.text import MIMEText
from config import EMAIL_PASSWORD

class EmailManger():
    def __init__(self):
        self.sender = 'baituantong@163.com'
        self.mail_host = 'smtp.163.com'
        self.mail_user = 'baituantong'
        self.mail_password = EMAIL_PASSWORD

    def send(self, receivers, message_text):
        try:
            message = self.wrap_message(message_text, receivers[0])
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(self.mail_user, self.mail_password)
            smtpObj.sendmail(self.sender, receivers, message.as_string())
            smtpObj.quit()
            return 'success'
        except smtplib.SMTPException as e:
            return e

    def wrap_message(self, message_text, receiver):
        title, content = message_text
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = title
        message['from'] = self.sender
        message['To'] = receiver
        return message


if __name__ == '__main__':
    emailManager = EmailManger()
    print(emailManager.send(['1652961256@qq.com'], ('hehe', 'gaga')))