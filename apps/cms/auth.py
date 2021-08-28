from functools import wraps
from flask import session, redirect, url_for, g
from config import CMS_USER_ID, FRONT_USER_ID


def login_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(CMS_USER_ID):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return wrapper


def access_auth(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if g.cms_user.has_permission(permission):
                return func(*args, **kwargs)
            return redirect(url_for('cms.index'))
        return inner
    return outter


def front_login_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('FRONT_USER_ID'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.login'))
    return wrapper
