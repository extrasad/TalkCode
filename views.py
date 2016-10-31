# coding=utf-8
from datetime import date
from flask import Flask, request, render_template, make_response, session, redirect, url_for, flash, jsonify
from flask_wtf import CsrfProtect
from form import RegisterForm, LoginForm, PersonalForm, CurriculumForm
from models import db, User, Personal_User, Curriculum_User
from flask_mysqldb import MySQL
from decorator import user_required

mysql = MySQL()
app = Flask(__name__)


#   Routes

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404


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
        user_personal_info = db.session.query(Personal_User).filter(User.id == session['id']).first()
        if user_personal_info == None: #Si no hay informacion personal
            return render_template('user.html', name_user=session['username'])
        else:
            name = str(user_personal_info.name) + ' ' + str(user_personal_info.last_name)
            info_personal = [name, user_personal_info.sex,\
                             user_personal_info.country, user_personal_info.city, user_personal_info.dob,\
                             user_personal_info.repository, user_personal_info.social_red]
            return render_template('user.html', name_user=session['username'], personal_info=info_personal)
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

        jquery_validate_username = User.query.filter_by(username=username).first()

        if jquery_validate_username is not None:
            uri_parameters = 'invalid'
            flash('That dates in use', 'danger')
            print uri_parameters
            return redirect(url_for('register', error=uri_parameters))
        else:
            session['username'] = username
            session['password'] = password
            session['email'] = email
            user_new = User(username=session['username'], password=session['password'], email=session['email'])
            db.session.add(user_new)
            db.session.commit()
            #   user_id, quitar si redirect esta haciendo que se ejecute bien la funcion user
            user_id = db.session.query(User.id).filter(User.username == session['username']).first()
            session['id'] = user_id[0]
            flash('Your user commit!', 'success')
            return redirect(url_for('user', name=username))
    else:
        return render_template('register.html', form=new_registerForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    new_Loginform = LoginForm(request.form)
    if request.method == 'POST' and new_Loginform.validate():
        username = new_Loginform.username.data
        password = new_Loginform.password.data

        user = User.query.filter_by(username=username).first()

        if user is not None and user.verify_password(password):
            flash('Bienvenido {}'.format(username), 'success') #test
            session['username'] = username
            user_id = db.session.query(User.id).filter(User.username == session['username']).first()
            session['id'] = user_id[0]
            print 'Bienvenido de nuevo {}'.format(username)
            return redirect(url_for('user', name=username))

        else:
            flash('Username or password invalid', 'danger')
            print 'Error ', '\nusername:{}\npassword:{}'.format(username, password)
            return redirect(url_for('login',))

    return render_template('login.html', form=new_Loginform)


@app.route('/setting/personal_info', methods=['GET', 'POST'])
@user_required
def setting_personal():
    new_PersonalForm = PersonalForm(request.form)
    if request.method == 'POST' and new_PersonalForm.validate():
        query = db.session.query(User.id).filter(User.username == session['username']).first()
        user_id = query[0]  # long integer delete 'L'
        name = new_PersonalForm.name.data
        last_name = new_PersonalForm.last_name.data
        sex = new_PersonalForm.sex.data
        country = new_PersonalForm.country.data
        city = new_PersonalForm.city.data
        dob = new_PersonalForm.dob.data
        repository = new_PersonalForm.repository.data
        social_red = new_PersonalForm.social_red.data

        setting_new = Personal_User(user_id, name, last_name, sex,
                                    country, city, dob,
                                    repository, social_red)

        db.session.add(setting_new)
        db.session.commit()

        flash('Your personal date is update', 'success')
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

        flash('Your personal date is update', 'sucess')
        return redirect(url_for('user'))
    return render_template('form_curriculum_user.html', form=new_CurriculumForm)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/logout')
@user_required
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/create_question/user/<string:username>', methods=['GET', 'POST'])
@user_required
def create_question(username):
    username = session['username']
    return render_template('create_question.html')


@app.route('/query/execute')
def query_execute():
    cur = mysql.connection.cursor()
    cur.execute('SELECT username FROM user where username = "carlosjazz"')
    rv = cur.fetchall()
    return jsonify(username=rv)


@app.route('/query/sqlalchemy/user')
def query_orm_id():
    user = db.session.query(User).filter(User.username == session['username']).first()
    info_user = [user.id, user.username, user.password, user.email]
    return jsonify({session['username']: info_user})


@app.route('/query/sqlalchemy/personal_info')
def query_orm_personal():
    user_personal_info = db.session.query(Personal_User).filter(User.id == session['id']).first()
    if user_personal_info == None:
        return 'No have personal info'
    else:
        info_personal = [user_personal_info.name, user_personal_info.last_name, user_personal_info.sex,\
                         user_personal_info.country, user_personal_info.city, user_personal_info.dob,\
                         user_personal_info.repository, user_personal_info.social_red]
        return jsonify({session['username']: info_personal})
