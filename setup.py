# coding=utf-8
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name='talkcode',
    version='1.0.0',
    license='GNU General Public License v3',
    author='Carlos Azuaje',
    author_email='carlosjazzc1@gmail.com',
    description='Web app for questions, snippets, articles and much code.',
    packages=find_packages('app'),
    package_dir={'': 'app'},
    platforms='any',
    install_requires=[
        'flask>=0.10',
        'flask_mysqldb',
        'flask_sqlalchemy',
        'sqlalchemy',
        'sqlalchemy_utils',
        'flask_script',
        'flask_migrate',
        'flask-login',
        'alembic',
        'pycountry',
        'flask_wtf',
        'wtforms_components',
        'wtforms',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
