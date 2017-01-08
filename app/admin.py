from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import *
from flask_security import current_user
from flask import request, redirect, abort, url_for
import os.path


class _Admin(Admin, ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    def add_model_view(self, model):
        self.add_view(ModelView(model, db.session))

    def add_model_views(self, models):
        for model in models:
            self.add_model_view(model)