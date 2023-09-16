from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email(to_email, subj, text):
    msg = MIMEMultipart()
    msg['From'] = 'mighty.hiper@yandex.ru'
    msg['To'] = 'vladnety134@gmail.com'
    msg['Subject'] = subj
    msg.attach(
        MIMEText(text, 'plain')
    )
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo('mighty.hiper@yandex.ru')
    server.login('mighty.hiper@yandex.ru', 'rtuctelaovikxwfs')
    server.auth_plain()
    server.send_message(msg)
    server.quit()


send_email('mighty.hiper@yandex.ru', 'Hello world!', 'I love you!')