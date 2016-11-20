# coding=utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from views import app
from models import db

migrate = Migrate(app, db)
#   Ver si este es el problema, o es que debo runear esto desde models
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/talkcode?charset=utf8&use_unicode=0'

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
