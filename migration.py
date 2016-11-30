# coding=utf-8
from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/talkcode?charset=utf8&use_unicode=0'
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
