from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import *
from flask_admin.contrib.fileadmin import FileAdmin
import os.path


class _Admin(Admin):
    def add_model_view(self, model):
        self.add_view(ModelView(model, db.session))

    def add_model_views(self, models):
        for model in models:
            self.add_model_view(model)


def create_admin(app):
    admin = _Admin(app, name='talkcode', template_mode='bootstrap3')
    admin.add_model_views([
        User, Personal_User, Curriculum_User,
        Skill, Question, TagQuestion,
        AnswerLong, Snippet, TagSnippet, Star,
        CommentSnippet, Upvote, Downvote,
        Answer_Downvote, Answer_Upvote
    ])

    path = os.path.join(os.path.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

