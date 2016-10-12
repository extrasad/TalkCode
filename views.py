# coding=utf-8
from datetime import date
from flask import Flask, request, render_template, make_response, session, redirect, url_for, flash
from flask_wtf import CsrfProtect
from form import RegisterForm, LoginForm, PersonalForm, CurriculumForm
from models import db, User, Personal_User, Curriculum_User
from flask_mysqldb import MySQL
from decorator import user_required

mysql = MySQL()
app = Flask(__name__)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')


@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['user', 'logout', 'setting']:
        redirect(url_for('login'))

    if 'username' in session and request.endpoint in ['register', 'login']:
        redirect(url_for('user'))


@app.route('/', methods=['GET'])
def index():
    today = date.today()
    if 'username' in session:
        return render_template('index.html', date=today, button='btn btn-info btn-raised', username=session['username'])
    else:
        return render_template('index.html', date=today, button='btn btn-info btn-raised')



@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' in session:
        return render_template('user.html', name_user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    new_registerForm = RegisterForm(request.form)
    if request.method == 'POST' and new_registerForm.validate():
        print RegisterForm
        username = new_registerForm.username.data
        password = new_registerForm.password.data
        email = new_registerForm.email.data

        session['username'] = username
        session['password'] = password
        session['email'] = email

        user_new = User(username=session['username'], password=session['password'], email=session['email'])
        db.session.add(user_new)
        db.session.commit()
        print 'New user register!'
        flash('New user register')
        return redirect(url_for('user', name=username))
    else:
        print "Invalid"
        flash('Invalid Date')
        return render_template('register.html', form=new_registerForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    new_Loginform = LoginForm(request.form)
    if request.method == 'POST' and new_Loginform.validate():
        username = new_Loginform.username.data
        password = new_Loginform.password.data

        user = User.query.filter_by(username=username).first()

        if user is not None and user.verify_password(password):
            succes_message = 'Bienvenido {}'.format(username)
            flash(succes_message)
            session['username'] = username
            print 'Bienvenido de nuevo {}'.format(username)
            return redirect(url_for('user', name=username))

        else:
            error_message = 'Username or password invalid'
            flash(error_message)
            print 'Error ', '\nusername:{}\npassword:{}'.format(username, password)
            return redirect(url_for('login',))

    return render_template('login.html', form=new_Loginform)


@app.route('/setting/personal_info', methods=['GET', 'POST'])
@user_required
def setting_personal():
    new_PersonalForm = PersonalForm(request.form)
    if request.method == 'POST' and new_PersonalForm.validate():
        name = new_PersonalForm.name.data
        last_name = new_PersonalForm.last_name.data
        sex = new_PersonalForm.sex.data
        country = new_PersonalForm.country.data
        city = new_PersonalForm.city.data
        dob = new_PersonalForm.dob.data
        repository = new_PersonalForm.repository.data
        social_red = new_PersonalForm.social_red.data

        setting_new = Personal_User(name, last_name, sex,
                                    country, city, dob,
                                    repository, social_red)

        db.session.add(setting_new)
        db.session.commit()

        message = 'Your personal info is update'
        flash(message)
        return redirect(url_for('user'))
    return render_template('form_personal.html', form=new_PersonalForm)

@app.route('/setting/curriculum_info', methods=['GET', 'POST'])
@user_required
def setting_curriculum():
    new_CurriculumForm = CurriculumForm(request.form)
    if request.method == 'POST' and new_CurriculumForm.validate():
        tittle = new_CurriculumForm.tittle.data
        first_skill = new_CurriculumForm.first_skill.data
        second_skill = new_CurriculumForm.second_skill.data
        other_skill = new_CurriculumForm.other_skill.data
        university = new_CurriculumForm.university.data
        years = new_CurriculumForm.years.data
        description = new_CurriculumForm.description.data

        setting_new = Curriculum_User(tittle, first_skill, second_skill,
                                      other_skill, university,
                                      years, description)

        db.session.add(setting_new)
        db.session.commit()

        message = 'Your personal info is update'
        flash(message)
        return redirect(url_for('user'))
    return render_template('form_curriculum_user.html', form=new_CurriculumForm)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    if 'username' in session:
        exit_message = 'User {}'.format(session['username'])
        flash(exit_message)
        session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/cookie')
def cookie():
    reponse = make_response(render_template('cookie.html'))
    reponse.set_cookie('custome_cookies', 'default_value')
    return render_template('cookie.html')

@app.route('/query')
def query():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM user_personal_info''')
    rv = cur.fetchall()
    return str(rv)


@app.route('/params')#Control de parametros con '?' y '&'
def params():
    param_1 = request.args.get('params1', 'Not Request')
    param_2 = request.args.get('params2', 'Not Request') #http://127.0.0.1:8000/params?params1=Parametro&params2=Metropara

    return 'Los parametros son:  {}, {}'.format(param_1, param_2)

@app.route('/course/')#Si no hay nada despues de course, se retorna el valor default de name
@app.route('/course/<name>/')#Control de parametros desde el metodo
@app.route('/course/<name>/<int:number>')# Validar ruta con int:
def course(name='Free Course everything!', number=' '):
    return 'Course: {} Capitulo: {} '.format(name, number)
"""
#Ejemplo de listas y variables
@app.route('/users/<name>')
def users(name='default'):
    lenguage = ['C/C++', 'Javascript', 'Python']
    skill = ['Game Developer', 'Web Developer']
    skillOn = True
    pass"""
