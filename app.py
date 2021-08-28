from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
from exts import db, mail
from flask_wtf import CSRFProtect
from flask_avatar import Avatar
import config

app = Flask(__name__)
app.config.from_object(config)

mail.init_app(app)
CSRFProtect(app)
db.init_app(app)
Avatar(app)

app.register_blueprint(front_bp)
app.register_blueprint(common_bp)
app.register_blueprint(cms_bp)
app.register_blueprint(ueditor_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

