import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog_post.config import Config
from flask_migrate import Migrate
from sqlalchemy import MetaData
from elasticsearch import Elasticsearch

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = "info"
mail = Mail()
migrate = Migrate()

CATEGORIES = [('AI', 'Artificial Intelligence'), ('PY', 'Python'), ('DS', 'Data Science'), ('ML', 'Machine Learning'),
              ('Other', 'Other')]


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from blog_post import models

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from blog_post.users.routes import users
    from blog_post.posts.routes import posts
    from blog_post.main.routes import main
    from blog_post.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
