from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_security import current_user

from models import *

# https://github.com/sasaporta/flask-security-admin-example/blob/master/main.py

# Customized User model for SQL-Admin
class UserAdmin(ModelView):

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

class MyFileAdmin(FileAdmin):
    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

class _Admin(Admin, UserAdmin):
    def add_model_view(self, model):
        self.add_view(UserAdmin(model, db.session))

    def add_model_views(self, models):
        for model in models:
            self.add_model_view(model)

def create_security_admin(app, path):
    admin = _Admin(app, name='talkcode', template_mode='bootstrap3')
    admin.add_model_views([
        User, Role, Personal_User, Curriculum_User,
        Skill, Question, TagQuestion,
        AnswerLong, Snippet, TagSnippet, Star,
        CommentSnippet, Upvote, Downvote,
        Answer_Downvote, Answer_Upvote
    ])

    admin.add_view(MyFileAdmin(path, '/static/', name='Static Files'))