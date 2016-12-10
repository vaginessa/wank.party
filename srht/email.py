import smtplib
import pystache
import os
import html.parser
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from flask import url_for

from srht.database import db
from srht.objects import User
from srht.config import _cfg, _cfgi

def send_invite(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP_SSL(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/invite") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), {
                'user': user,
                "domain": _cfg("domain"),
                "protocol": _cfg("protocol")
            })))
    message['Subject'] = "Your wank.party account is approved"
    message['From'] = _cfg("smtp-user")
    message['To'] = user.email
    smtp.sendmail(_cfg("smtp-user"), [ user.email ], message.as_string())
    smtp.quit()

def send_rejection(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP_SSL(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/reject") as f:
        message = MIMEText(f.read())
    message['Subject'] = "Your wank.party account has been rejected"
    message['From'] = _cfg("smtp-user")
    message['To'] = user.email
    smtp.sendmail(_cfg("smtp-user"), [ user.email ], message.as_string())
    smtp.quit()

def send_reset(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP_SSL(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/reset") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), {
                'user': user,
                "domain": _cfg("domain"),
                "protocol": _cfg("protocol"),
                'confirmation': user.passwordReset
            })))
    message['Subject'] = "Reset your wank.party password"
    message['From'] = _cfg("smtp-user")
    message['To'] = user.email
    smtp.sendmail(_cfg("smtp-user"), [ user.email ], message.as_string())
    smtp.quit()
