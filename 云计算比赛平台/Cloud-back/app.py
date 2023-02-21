from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import create_app
from flask import Flask
from apps.user.models import User
from apps.admin.models import Admin
from exts import db


app = create_app()
migrate = Migrate(app=app, db=db)
manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()