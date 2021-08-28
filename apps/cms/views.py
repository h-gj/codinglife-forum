import threading

from flask import Blueprint, views, render_template,request, session, redirect, url_for, g, jsonify

from utils.mail import mail_and_cache
from .forms import \
    LoginForm, ResetPwdForm, ResetEmailForm, \
    BannerForm, BannerModForm, BannerDelForm, \
    BoardForm, BoardModForm, BoardManageForm
from .models import CMSUser, CMSPermission, CMSRole
from .auth import login_auth, access_auth
from config import CMS_USER_ID
from exts import db, mail
from utils import restful, cache
from flask_mail import Message
from ..models import Banner, Board, Thread, Comment, HlThread
from flask_paginate import Pagination, get_page_parameter
from apps.front.models import FrontUser, BoardManage
import string
import random
bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_auth
def index():
    return render_template('cms/cms_index.html')


@bp.route('/profile/')
@login_auth
def get_profile():
    return render_template('cms/profile.html')


@bp.route('/logout/')
@login_auth
def logout():
    session.clear()
    return redirect(url_for('cms.login'))


@bp.route('/sendcaptcha/')
def send_captcha():
    email = request.args.get('email')
    import re
    if not re.match(r'^[a-z0-9-_.]+@([a-z0-9]+.)+[a-z]+$', email):
        return restful.params_error('请输入正确格式的邮箱')
    captcha = list(string.ascii_letters)
    captcha.extend(map(lambda x: str(x), list(range(10))))
    captcha = random.sample(captcha, 6)
    captcha = "".join(captcha)
    msg = Message('CodingLife', recipients=[email], body='您的验证码是：%s' % captcha)
    threading.Thread(target=mail_and_cache, args=(email, msg, captcha)).run()
    return restful.success(message='发送邮件成功')


@bp.route('/banner/')
@login_auth
def banner_manage():
    banners = Banner.query.order_by(Banner.priority.desc()).all()
    return render_template('cms/banner.html', banners=banners)


@bp.route('/add_banner/', methods=['POST'])
@login_auth
def add_banner():
    form = BannerForm(request.form)
    print(request.form)
    if form.validate():
        name = form.name.data
        img_url = form.img_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = Banner(name=name, img_url=img_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/mod_banner/', methods=['POST'])
@login_auth
def mod_banner():
    form = BannerModForm(request.form)
    if form.validate():
        name = form.name.data
        img_url = form.img_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        bid = form.bid.data
        banner = Banner.query.get(bid)
        if banner:
            banner.name = name
            banner.img_url = img_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error("此轮播图不存在")
    else:
        return restful.params_error(form.get_error())


@bp.route('/del_banner/', methods=['POST'])
@login_auth
def del_banner():
    form = BannerDelForm(request.form)
    if form.validate():
        bid = form.bid.data
        print(bid)
        banner = Banner.query.get(bid)
        if banner:
            db.session.delete(banner)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('此轮播图不存在')
    else:
        return restful.params_error(form.get_error())


@bp.route('/thread/')
@login_auth
@access_auth(CMSPermission.POSTER)
def thread_manage():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)*10
    end = (page-1)*10+10
    threads = Thread.query.order_by(Thread.create_time.desc()).slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=Thread.query.count())
    return render_template('cms/thread.html', threads=threads, pagination=pagination)


@bp.route('/hl_thread/', methods=['POST'])
@login_auth
def hl_thread():
    thread_id = request.form.get('thread_id')
    if not thread_id:
        return restful.params_error('请传入帖子ID')
    thread = Thread.query.get(thread_id)
    if not thread:
        return restful.params_error('此帖子不存在')
    hlthread = HlThread(thread_id=thread_id)
    db.session.add(hlthread)
    db.session.commit()
    return restful.success()


@bp.route('/dishl_thread/', methods=['POST'])
@login_auth
def dishl_thread():
    thread_id = request.form.get('thread_id')
    if not thread_id:
        return restful.params_error('请传入帖子ID')
    thread = Thread.query.get(thread_id)
    if not thread:
        return restful.params_error('此帖子不存在')
    hlthread = HlThread.query.filter_by(thread_id=thread_id).first()
    db.session.delete(hlthread)
    db.session.commit()
    return restful.success()


@bp.route('/del_thread/', methods=['POST'])
@login_auth
def del_thread():
    thread_id = request.form.get('thread_id')
    if not thread_id:
        return restful.params_error('请传入帖子ID')
    thread = Thread.query.get(thread_id)
    if not thread:
        return restful.params_error('此帖子不存在')
    db.session.delete(thread)
    db.session.commit()
    return restful.success()


@bp.route('/comment/')
@login_auth
@access_auth(CMSPermission.COMMENTER)
def comment_manage():
    comments = Comment.query.order_by(Comment.create_time.desc()).all()
    return render_template('cms/comment.html', comments=comments)


@bp.route('/del_comment/', methods=['POST'])
@login_auth
def del_comment():
    comment_id = request.form.get('comment_id')
    if not comment_id:
        return restful.params_error('请传入评论ID')
    comment = Comment.query.get(comment_id)
    if not comment:
        return restful.params_error('此评论不存在')
    db.session.delete(comment)
    db.session.commit()
    return restful.success()


@bp.route('/board/')
@login_auth
@access_auth(CMSPermission.BOARDER)
def board_manage():
    boards = Board.query.all()
    return render_template('cms/board.html', boards=boards)


@bp.route('/add_board/', methods=['POST'])
@login_auth
@access_auth(CMSPermission.BOARDER)
def add_board():
    form = BoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = Board(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/mod_board/', methods=['POST'])
@login_auth
@access_auth(CMSPermission.BOARDER)
def mod_board():
    form = BoardModForm(request.form)
    if form.validate():
        bdid = form.bdid.data
        name = form.name.data
        board = Board.query.get(bdid)
        if not board:
            return restful.params_error('此板块不存在')
        board.name = name
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/del_board/', methods=['POST'])
@login_auth
@access_auth(CMSPermission.BOARDER)
def del_board():
    bdid = request.form.get('bdid')
    if not bdid:
        return restful.params_error('请传入板块ID')
    board = Board.query.get(bdid)
    if not board:
        return restful.params_error('此板块不存在')
    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/fuser/')
@login_auth
@access_auth(CMSPermission.FRONTUSER)
def fuser_manage():
    users = FrontUser.query.all()
    return render_template('cms/fuser.html', users=users)


@bp.route('/del_fuser/')
@login_auth
def del_fuser():
    uid = request.args.get('uid')
    if not uid:
        return restful.params_error('请传入用户ID')
    user = FrontUser.query.get(uid)
    if not user:
        return get_page_parameter('用户不存在')
    db.session.delete(user)
    db.session.commit()
    return restful.success()


@bp.route('/buser/', methods=['GET', 'DELETE', 'PUT', 'POST'])
@login_auth
@access_auth(CMSPermission.CMSUSER)
def buser_manage():
    if request.method == 'GET':
        cms_users = CMSUser.query.all()
        cms_roles = CMSRole.query.all()
        for user in cms_users:
            setattr(user, 'role', ','.join([role.name for role in user.roles]))
        return render_template('cms/buser.html', users=cms_users, cms_roles=cms_roles)
    elif request.method == 'DELETE':
        uid = request.args.get('uid')
        cms_user = CMSUser.query.get(uid)
        print('cms_user', cms_user)
        db.session.delete(cms_user)
        db.session.commit()
        return restful.success()
    elif request.method == 'PUT':
        uid = request.args.get('uid')
        role_id = request.args.get('role_id')
        cms_user = CMSUser.query.get(uid)
        role = CMSRole.query.get(role_id)
        cms_user.roles = [role]
        db.session.commit()
        return restful.success()
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        role_id = request.form.get('role_id')
        role = CMSRole.query.get(role_id)
        print('role', role)
        user = CMSUser(username=username, password=password, email=email)
        role.users.append(user)
        db.session.add(user)
        db.session.commit()
        return restful.success()


@bp.route('/board_manager/')
@login_auth
@access_auth(CMSPermission.BOARD_MANAGER)
def board_manager_manage():
    # board_manages = BoardManage.query.all()
    boards = Board.query.all()
    for board in boards:
        board.__setattr__('board_manages', [ (board_manager.manager.username,  board_manager.id) for board_manager in board.board_managers])
    return render_template('cms/board_manager.html', boards=boards)


@bp.route('/board_manager/', methods=['POST'])
@login_auth
@access_auth(CMSPermission.BOARD_MANAGER)
def add_board_manager():
    form = BoardManageForm(request.form)
    if form.validate():
        bdid = form.bdid.data
        username = form.username.data
        user = FrontUser.query.filter_by(username=username).first()

        if BoardManage.query.filter_by(manager=user, board_id=bdid).first():
            return restful.params_error(message='用户已是该板块版主')
        board_manage = BoardManage(board_id=bdid, manager=user)
        db.session.add(board_manage)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/board_manager/', methods=['DELETE'])
@login_auth
@access_auth(CMSPermission.BOARD_MANAGER)
def del_board_manager():
    bmid = request.args.get('bmid')
    board_manage = BoardManage.query.get(bmid)
    db.session.delete(board_manage)
    db.session.commit()
    return restful.success()


@bp.route('/role/')
@login_auth
@access_auth(CMSPermission.ALL_PERMISSION)
def role_manage():
    return render_template('cms/role.html')


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user:
                if user.check_password(password):
                    session[CMS_USER_ID] = user.id
                    if remember:
                        session.permanent = True
                    return redirect(url_for('cms.index'))
                else:
                    return self.get(message='密码错误')
            else:
                return self.get(message='用户不存在')
        else:
            error = form.errors.popitem()[1][0]
            return self.get(message=error)


class ResetPwdView(views.MethodView):
    decorators = [login_auth]

    def get(self):
        return render_template('cms/resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            old_pwd = form.old_pwd.data
            new_pwd = form.new_pwd.data
            user_id = session.get(CMS_USER_ID)
            user = CMSUser.query.get(user_id)
            if user.check_password(old_pwd):
                user.password = new_pwd
                db.session.commit()
                return restful.success(message='success')
            else:
                return restful.params_error(message='原密码不正确')
        else:
            err = form.get_error().popitem()[1][0]
            return jsonify({'code': 400, 'message': err})


class ResetEmailView(views.MethodView):
    decorators = [login_auth]

    def get(self):
        return render_template('cms/resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            print(email)
            g.cms_user.email = email
            db.session.commit()
            return restful.success('邮箱更换成功')
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))