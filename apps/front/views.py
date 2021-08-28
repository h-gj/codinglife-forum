import re
import threading
from functools import reduce
from operator import add

import itsdangerous
from flask import (Blueprint, render_template,
                   views, session,
                   url_for, g, abort, redirect)

from exts import cache
from utils.recorder import record_thread_browse_log
from apps.front.forms import RegisterForm, LoginForm, ThreadForm, CommentForm, UpdateProfileForm, ChildCommentForm
from utils import restful, safeutils
from exts import db
from utils.mail import send_mail
from .models import FrontUser, GenderEnum, BoardManage
from ..models import Banner, Board, Thread, Comment, HlThread, ThreadLike, ThreadCollect, CommentLike
from ..cms.auth import front_login_auth
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import or_
from datetime import datetime
from sqlalchemy import func
import os, random, string
from qiniu import Auth, etag, put_file
from flask import request, jsonify
from werkzeug.utils import secure_filename
from config import QINIU_AK, QINIU_BUCKET, QINIU_SK, QINIU_DOMAIN
import config

bp = Blueprint('front', __name__)


@bp.app_errorhandler(404)
def handle_error(e):
    return render_template('front/404.html'), 404


@bp.app_template_filter(name='timedelta')
def time_delta(time):
    if isinstance(time, datetime):
        now = datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return '刚刚'
        elif 60 <= timestamp < 60 * 60:
            minutes = timestamp / 60
            return '%s 分钟前' % int(minutes)
        elif 60 * 60 <= timestamp < 60 * 60 * 24:
            hours = timestamp / (60 * 60)
            return '%s小时前' % int(hours)
        elif 60 * 60 * 24 <= timestamp < 60 * 60 * 24 * 30:
            days = timestamp / (60 * 60 * 24)
            return '%s天前' % int(days)
        else:
            return time.strftime('%Y/%m/%d/ %H:%M')


@bp.route('/qiniuupload/', methods=["GET", "POST"])
def qiniuupload():
    if request.method == "POST":
        up = UpFile()
        f = request.files["avatar"]
        filename = os.path.join(config.USER_AVATARS, secure_filename(f.filename))
        f.save(filename)
        mime = filename.rsplit(".")[1]
        qiniu_url = up.upload_img(filename, mime)

        if qiniu_url:
            user = FrontUser.query.get(g.front_user.id)
            user.avatar = 'https://' + qiniu_url
            db.session.commit()
            up.notify("qiniu-fileup", "图片上传成功")
            return jsonify({'code': 200, 'message': ''})
        else:
            up.notify("qiniu-fileup", "图片上传失败")
            return jsonify({'code': 400, 'message': 'Internal Server Error'})


class UpFile(object):
    @staticmethod
    def random_name():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

    def upload_img(self, fn, sfx):
        key = self.random_name() + "." + sfx
        q = Auth(QINIU_AK, QINIU_SK)
        token = q.upload_token(QINIU_BUCKET, key, 3600)
        ret, info = put_file(token, key, fn)
        if (ret is not None) and ret['key'] == key and ret['hash'] == etag(fn):
            return QINIU_DOMAIN + key
        else:
            self.notify("qiniu-fileup", "上传七牛云失败")
            return False

    @staticmethod
    def notify(title, text):
        os.system("osascript -e 'display notification \"{}\" with title \"{}\"'".format(text, title))


@bp.route('/')
@cache.cached(timeout=60, query_string=True)
def index():
    banners = Banner.query.order_by(Banner.priority.desc()).limit(4)
    boards = Board.query.all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    filter_by = request.args.get('filter_by', type=str, default='most-newest')
    if filter_by not in ['most-newest', 'well-chosen', 'liked-most', 'commented-most', 'browsed-most']:
        filter_by = 'most-newest'
    bid = request.args.get('bid', type=int, default=None)
    threads = None
    if filter_by == 'most-newest':
        threads = Thread.query.order_by(Thread.create_time.desc())
    elif filter_by == 'well-chosen':
        threads = db.session.query(Thread).outerjoin(HlThread).order_by(HlThread.create_time.desc(),
                                                                        Thread.create_time.desc())
    elif filter_by == 'liked-most':
        threads = db.session.query(Thread). \
            outerjoin(ThreadLike). \
            group_by(Thread.id). \
            order_by(func.count(ThreadLike.thread_id).desc(), Thread.create_time.desc())
    elif filter_by == 'commented-most':
        threads = db.session.query(Thread). \
            outerjoin(Comment). \
            group_by(Thread.id). \
            order_by(func.count(Comment.thread_id).desc(), Thread.create_time.desc())
    elif filter_by == 'browsed-most':
        threads = Thread.query.order_by(Thread.browse_num.desc())
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    if bid:
        threads_obj = threads.filter(Thread.board_id == bid)
        threads = threads_obj.slice(start, end)
        total = threads_obj.count()
    else:
        threads = threads.slice(start, end)
        total = Thread.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total)
    recommend = Thread.query.outerjoin(ThreadLike).outerjoin(Comment).group_by(Thread.id).order_by(
        func.count(ThreadLike.thread_id).desc(), func.count(Comment.thread_id).desc()).limit(7)

    tl = Thread.query.join(ThreadLike).\
        group_by(Thread.author_id).\
        order_by(func.count(ThreadLike.id).desc()).\
        slice(0, 5)
    most_liked_user = FrontUser.query.join(Thread).join(ThreadLike).group_by(FrontUser.id).order_by(func.count(ThreadLike.id).desc())[:3]
    # most_liked_user = [item.author for item in tl]
    for user in most_liked_user:
        user_threads = Thread.query.filter_by(author=user)
        total_thread_likes = reduce(add, [len(thread.likes) for thread in user_threads])
        # print('total_thread_likes', total_thread_likes)
        setattr(user, 'total_liked_num', total_thread_likes)
        # for _ in most_liked_user:
        # [setattr(user, 'total_liked_num', ThreadLike.query.filter_by(user_id=user.id).count()) for user in most_liked_user]
    context = {
        'banners': banners,
        'boards': boards,
        'threads': threads,
        'pagination': pagination,
        'board_id': bid,
        'filter_by': filter_by,
        'recommend': recommend,
        'most_liked_user': most_liked_user
    }
    return render_template('front/index.html', **context)


@bp.route('/profile/<string:id>/')
@front_login_auth
def profile(id):
    user = FrontUser.query.get(id)
    if not user:
        abort(404)
    last_ptime = user.threads[0].create_time if user.threads else ''
    return render_template('front/profile.html', user=user, last_ptime=last_ptime)


@bp.route('/updateprofile/<string:id>/', methods=['get', 'post'])
@front_login_auth
def update_profile(id):
    if request.method == 'GET':
        managed_boards = ','.join([board_manager.board.name for board_manager in BoardManage.query.filter_by(manager_id=g.front_user.id).all()])
        return render_template('front/updateprofile.html', managed_boards=managed_boards)
    form = UpdateProfileForm(request.form)
    if form.validate():
        username = form.username.data
        email = form.email.data
        gender = GenderEnum(request.form.get('gender'))
        qq = request.form.get('qq')
        user = FrontUser.query.filter_by(id=id).first()
        if user.email != email and FrontUser.query.filter_by(email=email).first():
            return restful.params_error('此邮箱已存在')
        if user.username != username and FrontUser.query.filter_by(username=username).first():
            return restful.params_error('用户名已存在')
        user.username = username
        user.email = email
        user.gender = gender
        user.qq = qq
        db.session.commit()
        return restful.success()
    return restful.params_error(form.get_error())


@bp.route('/threadlist/<string:uid>/')
@front_login_auth
def threadlist(uid):
    user = FrontUser.query.get(uid)
    if not user:
        return restful.params_error('Unregisterd user')
    threads = Thread.query.filter_by(author_id=uid).order_by(Thread.create_time.desc()).all()
    context = dict(items=threads, user=user, title='帖子')
    return render_template('front/itemlist.html', **context)


@bp.route('/search/')
def search():
    kw = request.args.get('kw')
    if not kw:
        return redirect(url_for('front.index'))
    threads_obj = Thread.query.filter(
        or_(Thread.title.like('%' + kw + '%'), Thread.content.like('%' + kw + '%'))).order_by(Thread.create_time.desc())
    threads = threads_obj.all()
    thread_count = threads_obj.count()
    return render_template('front/search.html', threads=threads, thread_count=thread_count)


@bp.route('/logout/')
@front_login_auth
def log_out():
    session.clear()
    return redirect(url_for('front.login'))


@bp.route('/thread/', methods=['GET', 'POST'])
@front_login_auth
def post():
    if request.method == 'GET':
        tid = request.args.get('tid')
        thread = None
        if tid:
            thread = Thread.query.get(tid)
        boards = Board.query.all()
        context = {
            'boards': boards,
            'thread': thread
        }
        return render_template('front/post.html', **context)
    else:
        form = ThreadForm(request.form)
        if form.validate():
            tid = request.form.get('tid')
            if tid:
                thread = Thread.query.get(tid)
                thread.title = form.title.data
                thread.content = form.content.data
                thread.board_id = form.board_id.data
                thread.is_edited = True
            else:
                title = form.title.data
                content = form.content.data
                board_id = form.board_id.data
                author_id = g.front_user.id
                thread = Thread(title=title, content=content, board_id=board_id, author_id=author_id)
                db.session.add(thread)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route('/thread/<thread_id>/')
@record_thread_browse_log
@cache.cached(timeout=60)
def thread_detail(thread_id):
    """帖子详情页"""
    thread = Thread.query.get(thread_id)
    if not thread:
        abort(404)
    thread.browse_num += 1
    db.session.commit()
    comments = Comment.query.filter_by(thread_id=thread.id, parent=None).order_by(Comment.create_time.desc()).all()
    is_liked = False
    is_collected = False
    is_board_manager=False 
    if g.get('front_user'):
        like = ThreadLike.query.filter_by(thread_id=thread_id, user_id=g.front_user.id).first()
        collection = ThreadCollect.query.filter_by(thread_id=thread_id, user_id=g.front_user.id).first()
        is_liked = True if like else False
        is_collected = True if collection else False
        is_board_manager = bool(BoardManage.query.filter_by(manager_id=g.front_user.id, board_id=thread.board_id).first())
    context = dict(thread=thread, comments=comments, is_liked=is_liked, is_collected=is_collected, is_board_manager=is_board_manager)
    return render_template('front/thread.html', **context)


@bp.route('/threads/comment/<comment_id>')
def get_paginated_comments(comment_id):
    page = int(request.args.get('page'))
    print(page)
    comment_per_page = 5
    comments = db.session.query(Comment).filter(Comment.parent_id == comment_id).order_by(Comment.create_time.desc())
    start = (page - 1) * comment_per_page
    end = start + comment_per_page
    print('start', start)
    print('end', end)
    print('comments', comments.all())
    paginated_comments = comments.slice(start, end)
    # print('paginated_comments', paginated_comments.all())
    com_info_list = [{
        'id': comment.id,
        'username': comment.author.username,
        'uid': comment.author.id,
        'content': comment.content,
        'create_time': time_delta(comment.create_time),
        'like_count': CommentLike.query.filter_by(comment_id=comment.id).count()
    } for comment in paginated_comments]

    return jsonify({'code': 200, 'message': '', 'data': com_info_list})


@bp.route('/delitem/')
@front_login_auth
def del_item():
    """帖子列表、收藏列表、详情页面中删除帖子的统一接口"""
    iid = request.args.get('iid')
    if not iid:
        return restful.params_error('请传入帖子ID')
    thread = Thread.query.filter_by(author_id=g.front_user.id, id=iid).first()

    if not thread:
        # 该帖子不是当前用户所发的，则判断是否当前用户收藏了该帖子
        thread = ThreadCollect.query.filter_by(user_id=g.front_user.id, thread_id=iid).first()
        th = Thread.query.filter_by(id=iid).first()
        if th:
            board_manager = BoardManage.query.filter_by(manager_id=g.front_user.id, board_id=th.board_id).first()
            if board_manager:
                thread = th
            elif not thread:
                abort(404)
    db.session.delete(thread)
    db.session.commit()
    return restful.success()


@bp.route('/add_comment/', methods=['POST'])
@front_login_auth
def add_comment():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        author_id = form.author_id.data
        thread_id = form.thread_id.data
        comment = Comment(content=content, author_id=author_id, thread_id=thread_id)
        db.session.add(comment)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/add_child_comment/', methods=['POST'])
@front_login_auth
def add_child_comment():
    form = ChildCommentForm(request.form)
    if form.validate():
        content = form.content.data
        author_id = form.author_id.data
        thread_id = form.thread_id.data
        parent_id = form.parent_id.data
        comment = Comment(content=content, author_id=author_id, thread_id=thread_id, parent_id=parent_id)
        db.session.add(comment)
        db.session.commit()
        # return restful.success()
        create_time = time_delta(comment.create_time)
        print(create_time)
        com_item_info = {
            'id': comment.id,
            'username': comment.author.username,
            'content': comment.content,
            'create_time': create_time}
        return jsonify({'code': 200, 'message': '', 'data': com_item_info})
    else:
        return restful.params_error(form.get_error())


@bp.route('/del_comment/<comment_id>', methods=['DELETE'])
@front_login_auth
def del_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        abort(404)
    db.session.delete(comment)
    db.session.commit()
    return restful.success()


@bp.route('/threads/comment-like/<comment_id>', methods=['POST'])
@front_login_auth
def like_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        abort(404)
    com_like = CommentLike(author_id=g.front_user.id, comment_id=comment_id)
    db.session.add(com_like)
    db.session.commit()
    return restful.success()


class RegisterView(views.MethodView):
    def get(self):
        if g.get('front_user'):
            return redirect(url_for('front.index'))
        referrer = request.referrer
        if referrer and referrer != url_for('front.login', _external=True) and safeutils.is_safe_url(referrer):
            next_to = referrer
        else:
            next_to = url_for('front.index')
        return render_template('front/register.html', next_to=next_to)

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password1.data
            email = form.email.data
            captcha = form.captcha.data
            if not captcha == cache.get(email):
                return restful.params_error('请输入正确的邮箱验证码')
            try:
                user = FrontUser(email=email, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                session['FRONT_USER_ID'] = user.id
                return restful.success()
            except:
                return restful.params_error('注册失败')
        else:
            return restful.params_error(form.get_error())


class LoginView(views.MethodView):
    def get(self):
        if g.get('front_user'):
            return redirect(url_for('front.index'))
        referrer = request.referrer
        if not (referrer and safeutils.is_safe_url(referrer)):
            referrer = url_for('front.index')
        print(referrer)
        return render_template('front/login.html', next_to=referrer)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            account = form.account.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter(or_(FrontUser.username == account, FrontUser.email == account)).first()
            if user and user.check_password(password):
                session['FRONT_USER_ID'] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error('邮箱或密码错误')
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


@bp.route('/like/<int:tid>')
@front_login_auth
def like(tid):
    like = ThreadLike.query.filter(ThreadLike.user_id == g.front_user.id, ThreadLike.thread_id == tid).first()
    if like:
        return restful.params_error('你已经赞过该帖子了')
    like = ThreadLike(user_id=g.front_user.id, thread_id=tid)
    try:
        db.session.add(like)
        db.session.commit()
    except:
        return restful.server_error()
    return restful.success()


@bp.route('/collect/<int:tid>')
@front_login_auth
def collect(tid):
    collect = ThreadCollect.query.filter(ThreadCollect.user_id == g.front_user.id,
                                         ThreadCollect.thread_id == tid).first()
    if collect:
        return restful.params_error('你已收藏过该帖子了')
    collect = ThreadCollect(user_id=g.front_user.id, thread_id=tid)
    try:
        db.session.add(collect)
        db.session.commit()
    except:
        return restful.server_error()
    return restful.success()


@bp.route('/collectlist/<string:uid>/')
@front_login_auth
def collectlist(uid):
    user = FrontUser.query.get(uid)
    if not user:
        return restful.params_error('用户未注册')
    threads = Thread.query.join(ThreadCollect).filter_by(user_id=uid).order_by(ThreadCollect.add_time.desc()).all()
    context = dict(items=threads, user=user, title='收藏')
    return render_template('front/itemlist.html', **context)


# 找回密码
@bp.route('/resetpwd', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        email = request.args.get('email')
        return render_template('front/resetpwd.html', email=email)

    email = request.form.get('email')
    if not re.match(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", email):
        return restful.params_error(message='邮箱格式不正确')

    user = FrontUser.query.filter_by(email=email).first()
    if not user:
        return restful.params_error(message='该邮箱尚未注册')

    t = itsdangerous.TimedJSONWebSignatureSerializer(config.SALT, expires_in=600)  # 过期时间600秒

    res = t.dumps({'email': email})
    token = res.decode()
    threading.Thread(target=send_mail, args=(email, request.host_url, token)).run()
    return restful.success()


# 验证token
@bp.route('/verify_token', methods=['GET', 'POST'])
def verify_token():
    if request.method == 'GET':
        return render_template('front/setnewpwd.html')

    token = request.args.get('t')
    newpwd = request.form.get('newpwd')
    if not (5 < len(newpwd) < 19):
        return restful.params_error(message='请设置6到18位长度的密码')

    t = itsdangerous.TimedJSONWebSignatureSerializer(config.SALT)
    try:
        email = t.loads(token)['email']
    except:
        return restful.params_error(message='token已失效')
    user = FrontUser.query.filter_by(email=email).first()
    user.password = newpwd
    db.session.commit()
    return restful.success()
