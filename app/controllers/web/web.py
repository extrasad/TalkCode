import os

from flask import Blueprint, send_from_directory, current_app, render_template

APP_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(APP_DIR, '../../../application/build/static')
TEMPLATE_FOLDER = os.path.join(APP_DIR, '../../../application/build/')

app = Blueprint('web', __name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')