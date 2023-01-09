import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from hciao.mailer.abstracts import Mailer


class SimpleMailer(Mailer):

    def __init__(self, host: str, login_id: str, login_pass: str):
        self.smtp = smtplib.SMTP(host, 587)
        self.smtp.starttls()
        self.login_id = login_id
        self.login_pass = login_pass
        self.attachments = None

    def login(self, login_id: str, login_pass: str):
        self.smtp.login(login_id, login_pass)

    def attachment(self, file_path: list):
        msg = MIMEMultipart()

        for file in file_path:
            part = MIMEBase('application', 'octet-stream')
            with open(file, 'rb') as f:
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={Path(file).name}")
            msg.attach(part)
        self.attachments = msg
        return self

    def send(self, to: str, subject: str, msg: str) -> bool:
        msg = MIMEText(msg)
        if self.attachments is not None:
            self.attachments.attach(msg)
            msg = self.attachments

        msg['Subject'] = subject

        try:
            self.login(self.login_id, self.login_pass)
            self.smtp.sendmail(self.login_id, to, msg.as_string())
            self.smtp.quit()

            return True
        except:
            return False
