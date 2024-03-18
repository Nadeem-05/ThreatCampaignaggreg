from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# creating app instance
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdfgh;lkjh'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)
    from .views import views

    app.register_blueprint(views, url_prefix="/")
    # database
    from .modals import Rssfeed
    create_database(app)
    return app


def create_database(app):
    if not path.exists('/home/nadeem/Desktop/Intern/rssfeed-aggreg/instance/database.db'):
        with app.app_context():
            db.create_all()
            print("database created!")
            
