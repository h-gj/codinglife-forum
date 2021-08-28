# coding: utf8

from flask_script import Manager
from app import app
from flask_migrate import Migrate, MigrateCommand

from apps.front.models import BoardManage
from apps.models import Board
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps import models
manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission
FrontUser = front_models.FrontUser


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def add_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('添加CMS用户成功！')


@manager.option('-u', '-username', dest='username')
@manager.option('-p', '-password', dest='password')
@manager.option('-e', '-email', dest='email')
def add_front_user(username, password, email):
    user = FrontUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('添加用户成功！')


@manager.command
def create_role():
    # visitor = CMSRole(name='访问者', desc='访问相关信息')
    # visitor.permission = CMSPermission.VISITOR
    #
    # operator = CMSRole(name='运营者', desc='管理帖子、评论和前台用户')
    # operator.permission = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER
    #
    # admin = CMSRole(name='管理员', desc='拥有全部权限')
    # admin.permission = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.CMSUSER | CMSPermission.FRONTUSER | CMSPermission.BOARDER
    #
    # developer = CMSRole(name='开发者', desc='拥有至高无上的权限')
    # developer.permission = CMSPermission.ALL_PERMISSION

    admin = CMSRole(name='总管理员', desc='拥有至高无上的权限')
    admin.permission = CMSPermission.ALL_PERMISSION

    operator = CMSRole(name='平台运营', desc='拥有除板块管理、CMS用户管理外的全部权限')
    operator.permission = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER

    db.session.add_all([operator, admin])
    db.session.commit()


@manager.option('-u', '-username', dest='username')
@manager.option('-r', '-role', dest='role')
def add_to_role(username, role):
    user = CMSUser.query.filter_by(username=username).first()
    role = CMSRole.query.filter_by(name=role).first()
    if user and role:
        role.users.append(user)
        db.session.commit()
        print('添加角色成功！')
    else:
        print('该用户不存在！')


@manager.option('-u', '-username', dest='username')
def has_permission(username):
    user = CMSUser.query.filter_by(username=username).first()
    if not user:
        print('该用户不存在！')
    if user.is_developer():
        print('该用户有超级管理员权限！')
    else:
        print('该用户无超级管理员权限！')


@manager.command
def add_thread():
    for x in range(100):
        title = '标题%s' % x
        content = '内容%s' % x
        author = FrontUser.query.first()
        board = models.Board.query.first()
        thread = models.Thread(title=title, content=content)
        thread.board = board
        thread.author = author
        db.session.add(thread)
        db.session.commit()
    print('成功添加100帖子！')


@manager.command
def add_comment():
    author_id = 'BLAogUDpCSsGCRBBrEQ6bX'
    thread_id = 119
    for x in range(10):
        comment = models.Comment(content='或或内容%s' % x, author_id=author_id, thread_id=thread_id)
        db.session.add(comment)
        db.session.commit()
    print('添加成功')


@manager.option('-u', '-username', dest='username')
@manager.option('-b', '-board', dest='board')
def add_board_manager(username, board):
    user = FrontUser.query.filter_by(username=username).first()
    if not user:
        print('该用户不存在！')
    board = Board.query.filter_by(name=board).first()
    if not board:
        print('板块不存在！')
    board_manger = BoardManage(manager_id=user.id, board_id=board.id)
    db.session.add(board_manger)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
