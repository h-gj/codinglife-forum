from .views import bp
from flask import session, g
from config import CMS_USER_ID
from .models import CMSUser, CMSPermission


@bp.before_request
def before_request():
    user_id = session.get(CMS_USER_ID)
    if user_id:
        user = CMSUser.query.get(user_id)
        g.cms_user = user


@bp.context_processor
def context_processor():
    return {'CMSPermission': CMSPermission}
