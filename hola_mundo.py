# coding=utf-8
from flask import Flask, request, render_template, make_response, session, redirect, url_for
import form

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET','POST'])
def index():
    if 'username' in session:
        username = session['username']
        print username
    return 'Error: You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    GeneralForm = form.GeneralForm(request.form)
    if request.method == 'POST' and GeneralForm.validate():
        session['username'] = GeneralForm.username.data
        return render_template('user.html')
    else:
        return render_template('index.html', form=GeneralForm)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('index'))

@app.route('/cookie')
def cookie():
    reponse = make_response(render_template('cookie.html'))
    reponse.set_cookie('custome_cookies', 'default_value')
    render_template('cookie.html')

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


if __name__ == '__main__':
    app.run(debug=True, port=8000)
