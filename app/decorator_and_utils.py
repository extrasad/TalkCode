# coding=utf-8
import re
import os.path
from functools import wraps
from flask import redirect, url_for, session
from urlparse import urlparse
import pycountry

list_website = ['github', 'facebook', 'twitter',
                'tumblr', 'plus.google', 'google',
                'linkedin', 'reddit']


def user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


def know_website(anchor):
    for site in list_website:
        if anchor.__contains__(site):
            return site
        else:
            return urlparse(anchor)[1]


def know_name_country(alpha2):
    for alpha in list(pycountry.countries):
        if alpha2.__contains__(alpha.alpha2):
            return alpha.name


def know_file_extension(file):
    try:
        no_validate = re.search('^.*\.(jpg|JPG|gif|GIF|doc|DOC|pdf|PDF|mp3|mp4|pyc)', file).group(0)
        return False
    except AttributeError:
        extension = os.path.splitext(file)[1]
        return extension[1:]


def know_lang(format):
    if format is False:
        return 'javascript'

    format = format.lower()
    if format in ['cs', 'c', 'cpp', 'mm', 'm', 'kt', 'java', 'nut', 'scala']: return 'clike'
    if format in ["build", "bzl", "py", "pyw"]: return 'python'
    if format in ["clj", "cljc", "cljx"]: return 'clojure'
    if format in ["cl", "lisp", "el"]: return 'commonlisp'
    if format in ['scss', 'sass']: return 'sass'
    if format in ['pm', 'pl']: return 'perl'
    if format in ['exs', 'ex']: return 'elixir'

    if format == 'js': return 'javascript'
    if format == 'cmake': return 'cobol'
    if format == 'squirrel': return 'squirrel'
    if format == 'ceylon': return 'ceylon'
    if format == 'sh': return 'shell'
    if format == 'erl': return 'erlang'
    if format == 'erl': return 'erlang'
    if format == 'coffee': return 'coffeescript'
    if format == 'cr': return 'crystal'
    if format == 'cbl': return 'cobol'
    if format == 'jl': return 'julia'
    if format == 'ls': return 'livescript'
    if format == 'hs': return 'haskell'
    if format == 'vb': return 'visualbasic'
    if format == 'rb': return 'ruby'
    if format == 'st': return 'smalltalk'
    if format == 'md': return 'markdown'

    if format in ['sql', 'r', 'php', 'go', 'd',
                  'css', 'groovy', 'yaml', 'dart',
                  'lua', 'swift', 'html', 'xml']: return format

    return 'javascript'  # default mode


def know_mode_exist(*args):
    for tag in args:
        if tag in ['html', 'xml', 'php']:
            tag = 'htmlmixed'
        if os.path.exists('./app/static/codemirror/mode/' + tag):
            return tag
    return 'javascript' # BUG:
