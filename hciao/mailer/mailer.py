import smtplib
from email.mime.text import MIMEText
from hciao.mailer.abstracts import Mailer


class SimpleMailer(Mailer):

    def __init__(self, host: str, login_id: str, login_pass: str):
        self.smtp = smtplib.SMTP(host, 587)
        self.smtp.starttls()
        self.login_id = login_id
        self.login_pass = login_pass
        self.is_login = False

    def login(self, login_id: str, login_pass: str):
        self.smtp.login(login_id, login_pass)
        self.is_login = True

    def send(self, to: str, subject: str, msg: str) -> bool:
        msg = MIMEText(msg)
        msg['Subject'] = subject

        if not self.is_login:
            self.login(self.login_id, self.login_pass)
        try:
            self.smtp.sendmail(self.login_id, to, msg.as_string())
            self.smtp.quit()

            return True
        except:
            return False
