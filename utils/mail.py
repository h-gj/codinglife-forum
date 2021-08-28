from flask_mail import Message
from exts import mail
from utils import cache


def send_mail(email, url, token):
    msg = Message('CodingLife - 找回密码', recipients=[email])
    msg.html = '<a href="{}verify_token?t={}">{}&nbsp;&nbsp;点击链接重置密码</a>'.format(url, token, token)
    try:
        mail.send(msg)
    except Exception as e:
        print('send_mail_error: ', e)


def mail_and_cache(email, msg, captcha):
    mail.send(msg)
    cache.set(email, captcha)
