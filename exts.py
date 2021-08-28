from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from config import CACHE_CONFIG

db = SQLAlchemy()
mail = Mail()
cache = Cache(config=CACHE_CONFIG)
