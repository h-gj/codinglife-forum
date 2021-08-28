from wtforms import StringField, IntegerField, Form, ValidationError
from wtforms.validators import Length, InputRequired, Email, EqualTo
from ..forms import BaseForm
from exts import cache
from apps.cms.models import CMSUser
from ..front.models import FrontUser, BoardManage


class LoginForm(BaseForm):
    email = StringField(validators=[Email()])
    password = StringField(validators=[Length(6, 20, message='请输入长度为6-20位的密码')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    old_pwd = StringField(validators=[Length(6, 20, message='请输入长度为6-20位的密码')])
    new_pwd = StringField(validators=[Length(6, 20, message='请输入长度为6-20位的密码')])
    new_pwd_repeat = StringField(validators=[EqualTo('new_pwd', message='两次密码输入不一致')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱')])
    captcha = StringField(validators=[Length(6, 6, message='请输入长度为6位的验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        if not captcha or captcha != cache.get(email):
            raise ValidationError('验证码不正确或已过期')

    def validate_email(self, field):
        email = field.data
        user = CMSUser.query.filter_by(email=email).first()
        if user:
            raise ValidationError('该邮箱已绑定其他账号')


class BannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入轮播图名称")])
    img_url = StringField(validators=[InputRequired(message="请输入图片链接")])
    link_url = StringField(validators=[InputRequired(message="请输入跳转链接")])
    priority = IntegerField(validators=[InputRequired(message="请输入权重")])


class BannerModForm(BannerForm):
    bid = IntegerField(validators=[InputRequired(message='请输入轮播图ID')])


class BannerDelForm(BaseForm):
    bid = IntegerField(validators=[InputRequired(message='请输入轮播图ID')])


class BoardForm(BaseForm):
    name = StringField(validators=[InputRequired('请输入板块名称')])


class BoardModForm(BoardForm):
    bdid = IntegerField(validators=[InputRequired(message='请输入板块ID')])


class BoardManageForm(BaseForm):
    bdid = IntegerField(validators=[InputRequired(message='请输入板块ID')])
    username = StringField(validators=[InputRequired('请输入用户名称')])

    def validate_username(self, field):
        user = FrontUser.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('用户不存在')
