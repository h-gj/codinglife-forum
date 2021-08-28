from exts import db
from datetime import datetime


class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Thread(db.Model):
    __tablename__ = 'thread'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    is_edited = db.Column(db.Boolean, default=False)
    browse_num = db.Column(db.Integer, default=0)

    board = db.relationship('Board', backref='threads')
    author = db.relationship('FrontUser', backref=db.backref('threads', cascade='all', order_by='Thread.create_time.desc()'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id =db.Column(db.String(100), db.ForeignKey('front_user.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent = db.relationship('Comment', remote_side=[id], backref=db.backref('children', cascade='all'))

    author = db.relationship('FrontUser', backref=db.backref('comments', cascade='all'))
    thread = db.relationship('Thread', backref=db.backref('comments', cascade='all'))


class CommentLike(db.Model):
    __tablename__ = 'comment_like'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))

    comment = db.relationship('Comment', backref=db.backref('likes', cascade='all'))
    author = db.relationship('FrontUser', backref=db.backref('comment_likes', cascade='all'))


class HlThread(db.Model):
    __tablename__ = 'hl_thread'
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    thread = db.relationship('Thread', backref='hlthread')


class ThreadLike(db.Model):
    __tablename__ = 'thread_like'
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    user_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))

    thread = db.relationship('Thread', backref='likes')
    user = db.relationship('FrontUser', backref=db.backref('thread_likes', cascade='all'))


# user_collect = db.Table(
#     'user_collect',
#     db.Column('user_id', db.String(100), db.ForeignKey('front_user.id')),
#     db.Column('collect_id', db.Integer, db.ForeignKey('thread_collect.id'))
# )


class ThreadCollect(db.Model):
    __tablename__ = 'thread_collect'
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    user_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    add_time = db.Column(db.DateTime, default=datetime.now)

    thread = db.relationship('Thread', backref='collects')
    user = db.relationship('FrontUser', backref='collects')


