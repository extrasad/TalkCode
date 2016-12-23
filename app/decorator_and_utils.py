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
    if format == 'cpp': return 'clike'
    if format == 'cs': return 'clike'
    if format == 'mm' or format == 'm': return 'clike'
    if format == 'kt': return 'clike'
    if format == 'java': return 'clike'
    if format == 'nut': return 'clike'
    if format == 'scala': return 'clike'
    if format in ["build", "bzl", "py", "pyw"]: return 'python'
    if format == 'js': return 'javascript'
    if format == 'html': return 'html'
    if format == 'c': return 'clike'
    if format == 'cmake': return 'cobol'
    if format == 'squirrel': return 'squirrel'
    if format == 'ceylon': return 'ceylon'
    if format in ["clj", "cljc", "cljx"]: return 'clojure'
    if format == 'sh': return 'shell'
    if format == 'pm' or format == 'pl': return 'perl'
    if format == 'exs' or format == 'ex': return 'elixir'
    if format == 'erl': return 'erlang'
    if format == 'erl': return 'erlang'
    if format == 'coffee': return 'coffeescript'
    if format == 'cr': return 'crystal'
    if format == 'cbl': return 'cobol'
    if format in ["cl", "lisp", "el"]: return 'commonlisp'
    if format == 'jl': return 'julia'
    if format == 'ls': return 'livescript'
    if format == 'hs': return 'haskell'
    if format == 'vb': return 'visualbasic'
    if format == 'rb': return 'ruby'
    if format == 'st': return 'smalltalk'
    if format == 'md': return 'markdown'
    if format == 'sql': return format
    if format == 'r': return format
    if format == 'php': return format
    if format == 'go': return format
    if format == 'd': return format
    if format == 'css': return format
    if format == 'scss': return format
    if format == 'sass': return format
    if format == 'groovy': return format
    if format == 'yaml': return format
    if format == 'dart': return format
    if format == 'lua': return format
    if format == 'swift': return format

    return 'javascript'  # default mode

#print know_lang(know_file_extension('hola.swift'))

def know_mode_exist(*args):
    for tag in args:
        if tag == 'html' or tag == 'php':
            tag = 'htmlmixed'
        if os.path.exists('./app/static/codemirror/mode/' + tag):
            return tag
    return 'javascript' # BUG:
