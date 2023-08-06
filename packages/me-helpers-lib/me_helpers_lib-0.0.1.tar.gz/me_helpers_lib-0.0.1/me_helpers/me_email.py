

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from . import me_secrets


def send_mail(subject, body=None, to=me_secrets.gmail, files_to_send=[]):
    FROM = me_secrets.gmail
    TO = to

    msg = MIMEMultipart("alternative")
    msg["From"] = FROM
    msg["To"] = TO
    msg["Subject"] = subject

    if body:
        text_part = MIMEText(body, "plain")
        msg.attach(text_part)

    for file_ in files_to_send:
        with open(file_, "rb") as f:
            data = f.read()
            attach_part = MIMEBase("application", "octet-stream")
            attach_part.set_payload(data)
        encoders.encode_base64(attach_part)
        filename = file_.split('\\')[-1]
        attach_part.add_header("Content-Disposition",
                               f"attachment; filename= {filename}")
        msg.attach(attach_part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(me_secrets.gmail, me_secrets.gmail_pw)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
