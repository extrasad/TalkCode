#  **Talkcode**
### Web Application to write questions, answers, create your snippets and share


---   

Packages Required

* flask>=0.10
* flask_mysqldb
* flask_sqlalchemy
* flask-assets
* flask-security
* pdfkit
* sqlalchemy
* sqlalchemy_utils
* flask_script
* flask_migrate
* flask-login
* alembic
* pycountry==1.5
* flask_wtf
* wtforms_components
* wtforms

Install packages

```python
python setup.py install

```

Run database and migrate repository


```python
python manage.py db init
python manage.py db upgrade

```

**Import**: pdfkit need [wkhtmltopdf](http://wkhtmltopdf.org/downloads.html)