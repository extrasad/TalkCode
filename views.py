# coding=utf-8
from flask import Flask, request, render_template, make_response, session, redirect, url_for, flash
from flask_wtf import CsrfProtect
import form
from config import DevelopmentConfig
from models import User, db
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect()
global skill
skill = []
mysql = MySQL(app)



#Crear index que sustituya a users como pagina de inicio


@app.errorhandler(404)
def page_not_found():
    return 'Page not found'

#Probar como resulta esta nueva funcion
@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['user']:
        redirect(url_for('login'))
        print '\033[94m'+'[the user need login]'.center(250)
    elif 'username' in session and request.endpoint in ['register', 'index']:
        redirect(url_for('user'))
    else:
        print '\033[94m'+'[   before_request  ]'.center(250)

@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' in session:
        username = session['username']
        print '\033[4m'+'{}'.format(username).center(250)
        GeneralForm = form.GeneralForm(request.form)
        if request.method == 'POST' and not GeneralForm.validate():
            session['skill'] = GeneralForm.skill.data
            skill.append(session['skill'])
            print '\033[4m'+'{}'.format(skill).center(250)
            return render_template('user.html', form=GeneralForm, name_user=session['username'], skill=skill)
        else:
            return render_template('user.html', form=GeneralForm, name_user=session['username'])
    else:
        return redirect(url_for('register')) #Login podria ser


@app.route('/register', methods=['GET', 'POST'])
def register():
    GeneralForm = form.GeneralForm(request.form)
    if request.method == 'POST' and not GeneralForm.validate():
        username = GeneralForm.username.data
        password = GeneralForm.password.data
        email = GeneralForm.email.data

        session['username'] = username
        session['password'] = password
        session['email'] = email

        user_new = User(username=session['username'],
                        password=session['password'],
                        email=session['email']
                        )
        db.session.add(user_new)
        db.session.commit()
        print '\033[92m'+'New user register!'.center(250)
        return redirect(url_for('user', name=username))
    else:
        return render_template('index.html', form=GeneralForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    Loginform = form.GeneralForm(request.form)
    if request.method == 'POST' and not Loginform.validate():
        username = Loginform.username.data
        password = Loginform.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            succes_message = 'Bienvenido {}'.format(username)
            flash(succes_message)
            session['username'] = username
            print '\033[92m'+'Bienvenido de nuevo {}'.format(username).center(250)
            return redirect(url_for('user', name=username))



        else:
            error_message = 'Username or password invalid'
            flash(error_message)
            print '\033[93m'+'Error','\033[91m'+'\nusername:{}\npassword:{}'.format(username, password).center(250)
            return redirect(url_for('login',))


    return render_template('login.html', form=Loginform)




@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    print session['username'].center(250)
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
    cur.execute('''SELECT email FROM user WHERE id > 0''')
    rv = cur.fetchall()
    return str(rv)

"""
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

#Ejemplo de listas y variables
@app.route('/users/<name>')
def users(name='default'):
    lenguage = ['C/C++', 'Javascript', 'Python']
    skill = ['Game Developer', 'Web Developer']
    skillOn = True
    pass
"""

if __name__ == '__main__':
    """run csrf sucurity"""
    csrf.init_app(app)
    """"run the SQLAlchemy.create_all() method to create the tables and database:"""
    db.init_app(app)
    """"Sincronizar la database con la aplicacion"""
    with app.app_context():
        db.create_all()

    db.init_app(app)
    app.run(port=8000)
