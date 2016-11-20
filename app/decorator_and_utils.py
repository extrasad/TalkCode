# coding=utf-8
import re
from functools import wraps
from flask import redirect, url_for, session
#   usar urllib2 y quitar esta mierda
list_website = ['github', 'facebook', 'twitter', 'plus.google', 'google']

def user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

def convert_uri_to_href(href):
    html = '<a href="{}">website</a>'.format(str(href))
    for site in list_website:
        if site in html:
            name_site = site
            html = html.replace('website', name_site)
            return html

def know_website(anchor):
    for site in list_website:
        if site in anchor:
            return site
