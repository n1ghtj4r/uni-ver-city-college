from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, current_user
from config import Config
import uuid

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)
    app.config['SERVER_BOOT_ID'] = str(uuid.uuid4())

    db.init_app(app)
    login_manager.init_app(app)

    @app.before_request
    def invalidate_stale_sessions():
        if current_user.is_authenticated and session.get('_boot_id') != app.config['SERVER_BOOT_ID']:
            logout_user()
            session.clear()

    from app.auth.routes import auth
    from app.student.routes import student
    from app.admin.routes import admin
    from app.api.routes import api

    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(admin)
    app.register_blueprint(api)

    return app