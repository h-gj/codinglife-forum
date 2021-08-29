from datetime import datetime

from exts import db
from werkzeug.security import check_password_hash, generate_password_hash
import shortuuid
import enum


class GenderEnum(enum.Enum):
    MALE = '男'
    FEMALE = '女'
    UNKNOW = '未知'


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(50), primary_key=True, default=shortuuid.uuid)
    # phone = db.Column(db.String(11), unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    # realname = db.Column(db.String(50))
    qq = db.Column(db.String(10))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    avatar = db.Column(db.String(50))
    signature = db.Column(db.String(100))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, raw_pwd):
        return check_password_hash(self.password, raw_pwd)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args, **kwargs)


class BoardManage(db.Model):
    __tablename__ = 'board_manager'
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    board = db.relationship('Board', backref=db.backref('board_managers', cascade='all'))
    manager = db.relationship('FrontUser', backref=db.backref('boards_managing', cascade='all'))


class ThreadBrowseLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id', ondelete='CASCADE'))
    request_ip = db.Column(db.String(15), nullable=True)
    user_id = db.Column(db.String(50), nullable=True)
    ua = db.Column(db.String(50), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
