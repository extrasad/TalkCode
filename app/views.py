# coding=utf-8
#   ------------------------------------- Modules ------------------------------
from . import app
from datetime import date
from flask import request, render_template, session, redirect, url_for, flash, jsonify
from form import *
from models import *
from flask_mysqldb import MySQL
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_admin import Admin, expose
from flask_admin.contrib.fileadmin import FileAdmin
from decorator_and_utils import user_required, know_website
import os.path

#   ------------------------------------- Instances ----------------------------
mysql = MySQL()
#   -------------------------------------- Admin -------------------------------
admin = Admin(app, name='talkcode', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Personal_User, db.session))
admin.add_view(ModelView(Curriculum_User, db.session))
admin.add_view(ModelView(Skills, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(TagQuestion, db.session))
admin.add_view(ModelView(AnswerLong, db.session))
admin.add_view(ModelView(Snippet, db.session))
admin.add_view(ModelView(TagSnippet, db.session))
admin.add_view(ModelView(CommentSnippet, db.session))
path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
# Handling request -------------------------------------------------------------


@app.errorhandler(404)
def page_not_found(e):
    """"No found"""
    return render_template('index.html'), 404


@app.before_request
def before_request():
    """Coment this function for debugging"""
    if 'username' not in session and request.endpoint in ['user', 'logout', 'setting']:
        redirect(url_for('login'))

    if 'username' in session and request.endpoint in ['register', 'login']:
        redirect(url_for('user'))

# Index ------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    today = date.today()
    if 'username' in session:
        return render_template('index.html', date=today, button='btn btn-info\
                               btn-raised', username=session['username'])
    else:
        return render_template('index.html', date=today, button='btn btn-info btn-raised')

# User Page --------------------------------------------------------------------
@app.route('/user/<string:username>', methods=['GET', 'POST'])
def user(username):
    """"Perfil del Usuario Logeado"""

    username = session['username']
    UserDate = User.query.filter_by(id=session['id']).first()
    PersonalDate = Personal_User.query.filter_by(id_user=session['id']).first()
    CurriculumDate = Curriculum_User.query.filter_by(id_user=session['id']).first()

    if PersonalDate is not None:
        user_link = [know_website(PersonalDate.social_red), know_website(PersonalDate.repository)]
        return render_template('user/user.html',
                               name_user=session['username'],
                               user_link=user_link,
                               PersonalDate=PersonalDate,
                               UserDate=UserDate,
                               CurriculumDate=CurriculumDate)

    return render_template('user/user.html', name_user=session['username'],
                           PersonalDate=PersonalDate,
                           UserDate=UserDate,
                           CurriculumDate=CurriculumDate)

# Sign in, Sign On, Sign out ---------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    new_registerForm = RegisterForm(request.form)
    if request.method == 'POST' and new_registerForm.validate():
        print RegisterForm
        username = new_registerForm.username.data
        password = new_registerForm.password.data
        email = new_registerForm.email.data

        query_validate_username = User.query.filter_by(username=username).first()
        query_validate_password = User.query.filter_by(password=password).first()
        query_validate_email = User.query.filter_by(email=email).first()


        if query_validate_username is not None or query_validate_password is not None or query_validate_email is not None:
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
            return redirect(url_for('user', username=username))
    else:
        return render_template('sign/register.html', form=new_registerForm)


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
            return redirect(url_for('user', username=username))

        else:
            flash('Username or password invalid', 'danger')
            print 'Error ', '\nusername:{}\npassword:{}'.format(username, password)
            return redirect(url_for('login',))

    return render_template('sign/login.html', form=new_Loginform)


@app.route('/logout')
@user_required
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))


# User Dates Form and More Things ----------------------------------------------


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
        return redirect(url_for('user', username=session['username']))
    return render_template('user/setting/form_personal.html',
                           form=new_PersonalForm)


@app.route('/setting/curriculum_info', methods=['GET', 'POST'])
@user_required
def setting_curriculum():
    """"Si esto da mas problemas hare dos add y ya..."""
    user = User.query.filter_by(id=session['id']).first()
    new_CurriculumForm = CurriculumForm(request.form, obj=user)
    if request.method == 'POST' and new_CurriculumForm.validate():
        tittle = new_CurriculumForm.tittle.data
        university = new_CurriculumForm.university.data
        description = new_CurriculumForm.description.data

        setting_new = Curriculum_User(session['id'], tittle,
                                      university, description)

        db.session.add(setting_new)
        db.session.commit()

        flash('Your personal date is update', 'success')
        return redirect(url_for('user', username=session['username']))
    return render_template('user/setting/form_curriculum_user.html',
                           form=new_CurriculumForm)
# About ----------------------------------------------------


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# Question  ------------------------------------------------


@app.route('/questions', methods=['GET', 'POST'])
@app.route('/questions/page/<int:page>', methods=['GET', 'POST'])
def questions_pagination(page=1):
    query_questions = Question.query.paginate(page, 3, False)
    return render_template('questions/questions_pagination.html',
                           questions=query_questions)


@app.route('/questions/id/<int:id>', methods=['GET', 'POST'])
def questions(id):
    new_answer_form = AnswerForm(request.form)

    question_data = db.session.query(Question).filter(Question.id == id).first()
    User_data = User.query.filter_by(id=question_data.id_user).first()
    Tag_data = TagQuestion.query.filter_by(id_question=question_data.id).first()

    all_Answers = AnswerLong.query.filter_by(id_question=id).all()


    if request.method == 'GET' and (session['id'] == User_data.id):

        return render_template('questions/question.html',
                               Answers=all_Answers,
                               User=User_data,
                               Question_data=question_data,
                               Tag=Tag_data)

    elif request.method == 'POST' and new_answer_form.validate():
        id_question = question_data.id
        answer_text = new_answer_form.answer_long.data
        answer_code = new_answer_form.text_area.data
        answer_new = AnswerLong(session['id'], session['username'],
                                id_question, answer_text, answer_code)

        db.session.add(answer_new)
        db.session.commit()
        flash('New answer!', 'success')
        return redirect(url_for('questions', id=id))

    else:
        return render_template('questions/question.html',
                               Answers = all_Answers,
                               answer_long=new_answer_form,
                               User=User_data,
                               Question_data=question_data,
                               Tag=Tag_data)

@app.route('/questions/write/user/<string:username>', methods=['GET', 'POST'])
@user_required
def create_question(username):
    username = session['username']
    new_QuestionForm = QuestionForm(request.form)
    if request.method == 'GET':
        flash('write your question!', 'info')
    if request.method == 'POST' and new_QuestionForm.validate():
        query = db.session.query(User.id).filter(User.username == session['username']).first()
        user_id = query[0]  # long integer delete 'L'
        title = new_QuestionForm.tittle.data
        description = new_QuestionForm.description.data
        text_area = new_QuestionForm.text_area.data
        question_new = Question(user_id, title, description, text_area)

        db.session.add(question_new)

        id_question = db.session.query(Question.id).filter(Question.id_user == session['id'], Question.title == title).first()
        id_question_for_tag = id_question[0]
        tag_new = TagQuestion(id_question_for_tag, new_QuestionForm.tag_one.data, new_QuestionForm.tag_two.data, new_QuestionForm.tag_three.data)
        db.session.add(tag_new)
        db.session.commit()
        flash('Perfect', 'info')
        id = db.session.query(Question.id).filter(Question.id_user == session['id'], Question.title == title).first()
        return redirect(url_for('questions', id=id[0]))
    return render_template('questions/create_question.html', form=new_QuestionForm)

# Snippets ---------------------------------------------------------------------


@app.route('/snippets/pagination')
def snippets_pagination():
    return "<h1>:(</h4>"


@app.route('/snippets/id/<int:id>', methods=['GET', 'POST'])
def snippets(id):
    new_comment_form = SnippetsComment(request.form)

    snippet_data = db.session.query(Snippet).filter(Snippet.id == id).first()
    User_data = User.query.filter_by(id=snippet_data.id_user).first()
    Tag_data = TagSnippet.query.filter_by(id_snippet=snippet_data.id).first()
    create_date = str(snippet_data.create_date).split(" ")[0]

    all_Comments = CommentSnippet.query.filter_by(id_snippet=id).all()

    if request.method == 'GET' and (session['id'] == User_data.id):
        return render_template('snippets/snippet.html',
                               Comments=all_Comments,
                               User=User_data,
                               Snippet_data=snippet_data,
                               Tag=Tag_data,
                               create_date=create_date)

    elif request.method == 'POST' and new_comment_form.validate():
        id_snippets = snippet_data.id
        comment_text = new_comment_form.comment.data
        comment_new = CommentSnippet(session['id'], id_snippets,
                                     session['username'],
                                     comment_text.upper())

        db.session.add(comment_new)
        db.session.commit()
        flash('New comment!', 'success')
        return redirect(url_for('snippets', id=id))

    else:
        return render_template('snippets/snippet.html',
                               Comments=all_Comments,
                               comment_form=new_comment_form,
                               User=User_data,
                               Snippet_data=snippet_data,
                               Tag=Tag_data,
                               create_date=create_date)


@app.route('/snippets/write/user/<string:username>', methods=['GET', 'POST'])
def create_snippet(username):
    username = session['username']
    new_SnippetForm = SnippetsForm(request.form)
    if request.method == 'GET':
        flash('write your snippet!', 'info')
    if request.method == 'POST' and new_SnippetForm.validate():
        query = db.session.query(User.id).filter(User.username == session['username']).first()
        user_id = query[0]  # long integer delete 'L'
        title = new_SnippetForm.tittle.data
        description = new_SnippetForm.description.data
        text_area = new_SnippetForm.text_area.data
        snippet_new = Snippet(user_id, title, description, text_area)

        db.session.add(snippet_new)

        id_snippet = db.session.query(Snippet.id).filter(Snippet.id_user == session['id'], Snippet.title == title).first()
        id_snippet_for_tag = id_snippet[0]
        tag_new = TagSnippet(id_snippet_for_tag, new_SnippetForm.tag_one.data, new_SnippetForm.tag_two.data, new_SnippetForm.tag_three.data)
        db.session.add(tag_new)
        db.session.commit()
        flash('Perfect', 'info')
        id = db.session.query(Snippet.id).filter(Snippet.id_user == session['id'], Snippet.title == title).first()
        return redirect(url_for('snippets', id=id[0]))
    return render_template('snippets/create_snippet.html', form=new_SnippetForm)


# Articles  --------------------------------------------------------------------


@app.route('/articles/pagination')
def articles_pagination():
    return "<h1>:(</h4>"

@app.route('/articles')
def articles():
    return render_template('articles/articles.html')

@app.route('/articles/write/user/<string:username>', methods=['GET', 'POST'])
def create_articles(username):
    username = session['username']
    return render_template('articles/create_article.html')


# Query Debbuging  -------------------------------------------------------------


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
    user_personal_info = db.session.query(Personal_User).filter(Personal_User.id_user == session['id']).first()
    if user_personal_info == None:
        return 'No have personal info'
    else:
        info_personal = [user_personal_info.name, user_personal_info.last_name, user_personal_info.sex,\
                         user_personal_info.country, user_personal_info.city, user_personal_info.dob,\
                         user_personal_info.repository, user_personal_info.social_red]
        return jsonify({session['username']: info_personal})
