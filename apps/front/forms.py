from wtforms import Form, StringField, IntegerField
from wtforms.validators import Regexp, InputRequired, EqualTo, ValidationError, Email, Length
from exts import cache
from apps.forms import BaseForm
import hashlib


class SendSMSForm(Form):
    salt = 'fdjfjdjgdgd5g4f4d5'
    phone = StringField(validators=[Regexp(r'^1[3456789]\d{9}$')])
    timestamp = StringField(validators=[Regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        if not super(SendSMSForm, self).validate():
            return False
        phone = self.phone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        encry_sign = hashlib.md5((phone + timestamp + self.salt).encode('utf-8')).hexdigest()
        if sign == encry_sign:
            return True
        else:
            return False


class RegisterForm(BaseForm):
    email = StringField(validators=[Email('请输入正确格式的邮箱')])
    captcha = StringField(validators=[InputRequired(message='请输入6位邮箱验证码')])
    username = StringField(validators=[Regexp(r'^.{2,10}$', message='请输入2-10位长度的用户名')])
    password1 = StringField(validators=[Regexp(r'^[a-zA-Z0-9_-]{6,20}$', message='请输入6-20位正确格式的密码')])
    password2 = StringField(validators=[EqualTo('password1')])
    img_captcha = StringField(validators=[Regexp(r'[a-zA-Z0-9]{4}', message='请输入4位图形验证码')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        phone = self.phone.data
        captcha = cache.get(phone)
        if not captcha or captcha.lower() != sms_captcha.lower():
            raise ValidationError('短信验证码不正确')

    def validate_img_captcha(self, field):
        img_captcha = field.data
        if not img_captcha:
            raise ValidationError('请输入正确的图形验证码')


class LoginForm(BaseForm):
    account = StringField(validators=[InputRequired(message='请输入用户名或邮箱')])
    password = StringField(validators=[Regexp(r'^[a-zA-Z0-9_-]{6,20}$', message='请输入6-20位的密码')])
    remember = StringField()


class ThreadForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入帖子标题')])
    content = StringField(validators=[InputRequired(message='请输入帖子内容')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块ID')])


class CommentForm(BaseForm):
    content = StringField(validators=[InputRequired('请输入评论内容')])
    author_id = StringField(validators=[InputRequired('请输入作者ID')])
    thread_id = IntegerField(validators=[InputRequired('请输入帖子ID')])


class ChildCommentForm(CommentForm):
    parent_id = IntegerField(validators=[InputRequired('请输入父评论ID')])


class UpdateProfileForm(BaseForm):
    username = StringField(validators=[Regexp(r'^.{2,10}$', message='请输入正确格式的用户名')])
    email = StringField(validators=[Email('请输入正确格式的邮箱')])
    # phone = StringField(validators=[Regexp(r'^1[3456789]\d{9}$', message='请输入正确格式的手机号！')])
    # qq = StringField(validators=[Regexp(r'[123456789]\d{4,9}', message='请输入正确格式的QQ号！')])
    # gender = StringField(validators=[Regexp(r'[男女(未知)]')])
