from flask import Flask

import settings
from apps.admin.view import admin_bp
from apps.user.view import user_bp
from exts import db


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.Config)
    db.init_app(app=app)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    # print(app.url_map)
    return app