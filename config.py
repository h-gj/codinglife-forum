import os
import env

HOSTNAME = os.environ['db_host']
PORT = os.environ['db_port']
DATABASE = os.environ['db_name']
USERNAME = os.environ['db_user']
PASSWORD = os.environ['db_pass']
HOST = '0.0.0.0'


DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE)
SECRET_KEY = os.environ['SECRET_KEY']
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
CMS_USER_ID = os.environ['CMS_USER_ID']
FRONT_USER_ID = os.environ['FRONT_USER_ID']

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAIL_SUPPRESS_SEND = False
MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']

UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'imgs')
UEDITOR_UPLOAD_TO_QINIU = False
UEDITOR_QINIU_ACCESS_KEY = ""
UEDITOR_QINIU_SECRET_KEY = ""
UEDITOR_QINIU_BUCKET_NAME = ""
UEDITOR_QINIU_DOMAIN = ""

PER_PAGE = 10

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'upload')
USER_AVATARS = os.path.join(os.path.dirname(__file__), 'imgs')

QINIU_AK = os.environ['QINIU_AK']
QINIU_SK = os.environ['QINIU_SK']
QINIU_BUCKET = os.environ['QINIU_BUCKET']
QINIU_DOMAIN = os.environ['QINIU_DOMAIN']

 
# 生成token加的salt
SALT = os.environ['SALT']

CACHE_HOST = os.environ['cache_host']
