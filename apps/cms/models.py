from exts import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


class CMSPermission(object):
    ALL_PERMISSION = 0b11111111
    VISITOR        = 0b00000001
    POSTER         = 0b00000010
    COMMENTER      = 0b00000100
    BOARDER        = 0b00001000
    FRONTUSER      = 0b00010000
    CMSUSER        = 0b00100000
    BOARD_MANAGER  = 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    permission = db.Column(db.Integer, default=CMSPermission.VISITOR)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    users = db.relationship('CMSUser', secondary='cms_role_user', backref='roles')


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permission = 0
        for role in self.roles:
            all_permission |= role.permission
        return all_permission

    def has_permission(self, permission):
        return permission == self.permissions & permission

    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)
