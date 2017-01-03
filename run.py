# coding=utf-8
from app import app

def run_https():
    from werkzeug.serving import make_ssl_devcert
    make_ssl_devcert('./ssl', host='localhost')
    app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'))

def run_http():
    app.run(port=8000, debug=True)

run_http()