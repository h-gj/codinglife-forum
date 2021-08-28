from .views import bp
from flask import session, g, render_template
from apps.front.models import FrontUser


@bp.before_request
def before_request():
    front_user_id = session.get('FRONT_USER_ID')
    if front_user_id:
        user = FrontUser.query.get(front_user_id)
        g.front_user = user


@bp.errorhandler
def handle_error():
    return render_template('front/404.html'), 404
