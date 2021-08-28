# Flask论坛系统


#### 介绍

基于Flask Web框架开发的论坛系统。前端使用Bootstrap、Jquery、AJAX等技术，数据库使用Mysql，使用Flask caching插件存储图形验证码和邮箱验证码。
该项目采用B/S模型开发。该系统前台包括帖子的展示（最新帖子、点赞最多、评论最多）以及用户注册登录模块和收藏点赞删除评论功能；后台是基于管理员权限的CMS，不同身份具有不同的管理级别，管理内容有论坛版块、轮播图、帖子、前台用户、后台用户。


#### 安装教程

pip install requirements.txt


#### 使用说明
Prerequisite:
python installed
mysql installed

Setup:
git pull
pip install -r requirements.txt


create a file named env.py under project root directory and past following config(You should replace empty values with your specific config):

```shell
import os

os.environ['db_host'] = ''
os.environ['db_port'] = ''
os.environ['db_name'] = ''
os.environ['db_user'] = ''
os.environ['db_pass'] = ''
os.environ['cache_host'] = ''
os.environ['SECRET_KEY'] = ''
os.environ['CMS_USER_ID'] = ''
os.environ['FRONT_USER_ID'] = ''
os.environ['MAIL_USERNAME'] = ''
os.environ['MAIL_PASSWORD'] = ''
os.environ['MAIL_DEFAULT_SENDER'] = ''
os.environ['QINIU_AK'] = ''
os.environ['QINIU_SK'] = ''
os.environ['QINIU_BUCKET'] = ''
os.environ['QINIU_DOMAIN'] = ''
os.environ['SALT'] = ''
```

python manage.py db init
python manage.py db migrate
python manage.py db upgrade
flask run
