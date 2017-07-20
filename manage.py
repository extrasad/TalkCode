# coding=utf-8
from flask_script import Manager
from flask_assets import ManageAssets
from flask_migrate import Migrate, MigrateCommand

from run import app
from app.models import db

migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI']
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets)

if __name__ == '__main__':
    manager.run()
