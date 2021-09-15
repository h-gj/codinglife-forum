# Forum System Based On Flask/Bootstrap
Completed in my senior year back in college. I finished this project by following a video lesson and add some extra functions and styling a lot by myself.

## Tech Stack
- Python
- Flask
- Bootstrap
- JQuery
- AJAX
- Nginx
- uWSGI
- Docker

## Give a Glance
- Home Page: 
[![4eGnbT.png](https://z3.ax1x.com/2021/09/16/4eGnbT.png)](https://imgtu.com/i/4eGnbT)

- Thread Detail Page:
[![4eGGx1.png](https://z3.ax1x.com/2021/09/16/4eGGx1.png)](https://imgtu.com/i/4eGGx1)

- Threads Management Page: 
[![4eGwIe.png](https://z3.ax1x.com/2021/09/16/4eGwIe.png)](https://imgtu.com/i/4eGwIe)

## Intro
A simple forum where you can view threads, share threads and post your own threads and other features a normal forum system should have.
There is also a admin system where you can manage website content.
Your can give a role to a created admin. And admin with that role can manage content within their permission access.


## Setup
- git pull
- cd codinglife-forum
- (Optional) create a virtual env for this project
- pip install -r requirements.txt
- create config file

create a file named env.py under project root directory and paste following config(You should replace empty values with your specific config):

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

- python manage.py db init
- python manage.py db migrate
- python manage.py db upgrade
- flask run / python app.py
