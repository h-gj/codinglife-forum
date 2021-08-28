from functools import wraps

from flask import request, session

from apps.front.models import ThreadBrowseLogs
from exts import db


def record_thread_browse_log(f):
    @wraps(f)
    def inner(*arg, **kwargs):
        tbl = ThreadBrowseLogs(thread_id=request.view_args.get('thread_id'),
                               user_id=session.get('FRONT_USER_ID'),
                               request_ip=request.remote_addr,
                               ua=(request.headers.get('User-Agent') or '')[:50])
        db.session.add(tbl)
        db.session.commit()
        return f(*arg, **kwargs)

    return inner
