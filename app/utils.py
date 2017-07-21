# coding=utf-8
from flask_mysqldb import MySQL

from urlparse import urlparse

from models import Notification, db
from events import redis_store

import pycountry, re, os.path


mysql = MySQL()

list_website = ['github', 'facebook', 'twitter',
                'tumblr', 'plus.google', 'google',
                'linkedin', 'reddit']


def create_notification(id_user, text, url):
    # Create and check if redis have the user sid
    notification = Notification(id_user=id_user, text=text, url=url)
    db.session.add(notification)
    db.session.commit()

    socket_id = redis_store.get("user-%s" % id_user)

    if redis_store.get("user-%s" % id_user) != 'nil':
        return [socket_id, notification.serialize]
    else:
        return [False]

def exec_query(query_string):
    cur = mysql.connection.cursor()
    cur.execute(query_string)
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    return r


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
    if format in ['cs', 'c', 'cpp', 'mm', 'm', 'kt', 'java', 'x-jsp', 'nut', 'scala']: return 'clike'
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
    return 'javascript'


def know_mode_exist(*args):
    for tag in args:
        if tag in ['html', 'xml', 'php']: tag = 'htmlmixed'
        if tag in ['node', 'nodejs', 'expressjs', 'jquery', 'underscorejs', 'canvas']: tag = 'javascript'
        if tag == 'django': tag = 'python'
        if os.path.exists('./app/static/codemirror/mode/' + tag):
            return tag
    return 'javascript'