# coding=utf-8
#   ------------------------------------- Modules ------------------------------
from . import app, csrf
from datetime import date
from flask import request, render_template, session, redirect, url_for, flash, jsonify, json
from form import *
from models import *
from flask_mysqldb import MySQL
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_admin import Admin, expose
from flask_admin.contrib.fileadmin import FileAdmin
from decorator_and_utils import *
import os.path
import pycountry
from sqlalchemy import desc, asc, and_, or_, not_


#   ------------------------------------- Instances ----------------------------
mysql = MySQL()
#   -------------------------------------- Admin -------------------------------
admin = Admin(app, name='talkcode', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Personal_User, db.session))
admin.add_view(ModelView(Curriculum_User, db.session))
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


# Index ------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        UserDate = User.query.filter_by(username=session['username']).first()
        try:
            Questions_by_following = UserDate.followed_question().all()
            Answers_by_following = UserDate.followed_answer().all()
        except AttributeError:
            Questions_by_following, Answers_by_following = []

        return render_template('index.html',
                               Questions=Questions_by_following,
                               Answers=Answers_by_following,
                               button='btn btn-info, btn-raised',
                               username=session['username']
                               )
    else:
        return render_template('index.html')


# User Page --------------------------------------------------------------------
@app.route('/user/<string:username>', methods=['GET', 'POST'])
def user(username):
    UserDate = User.query.filter_by(username=username).first()
    PersonalDate = Personal_User.query.filter_by(id_user=UserDate.id).first()
    CurriculumDate = Curriculum_User.query.filter_by(id_user=UserDate.id).first()

    Questions = db.session.query(Question.title, Question.description, Question.create_date). \
        filter_by(id_user=UserDate.id). \
        order_by(desc(Question.create_date)). \
        limit(5)

    Snippets = db.session.query(Snippet.title, Snippet.description, Snippet.create_date). \
        filter_by(id_user=UserDate.id). \
        order_by(desc(Snippet.create_date)). \
        limit(5)

    Answers = db.session.query(AnswerLong.answer, Question.title). \
        filter(AnswerLong.id_user == UserDate.id). \
        filter(AnswerLong.id_question == Question.id). \
        order_by(desc(AnswerLong.create_date)). \
        limit(5)

    try:
        country = know_name_country(PersonalDate.country)
    except AttributeError:
        country = ' '

    if PersonalDate is not None:
        user_link = [know_website(PersonalDate.social_red), know_website(PersonalDate.repository)]
    else:
        user_link = ['', '']

    try:
        if request.method == 'GET' and (session['id'] == UserDate.id):
            return render_template('user/user.html',
                                   user_link=user_link,
                                   PersonalDate=PersonalDate,
                                   country=country,
                                   UserDate=UserDate,
                                   Questions=Questions,
                                   Snippets=Snippets,
                                   Answers=Answers,
                                   CurriculumDate=CurriculumDate,
                                   CRUD=True)
    except KeyError:
        pass

    return render_template('user/user.html',
                           user_link=user_link,
                           country=country,
                           PersonalDate=PersonalDate,
                           UserDate=UserDate,
                           Questions=Questions,
                           Snippets=Snippets,
                           Answers=Answers,
                           CurriculumDate=CurriculumDate,
                           CRUD=False,
                           is_authenticated=True if 'username' in session else False)


# Sign in, Sign On, Sign out ---------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    new_registerForm = RegisterForm(request.form)
    if request.method == 'POST' and new_registerForm.validate():
        username = new_registerForm.username.data
        password = new_registerForm.password.data
        email = new_registerForm.email.data

        query_validate_username = User.query.filter_by(username=username).first()
        query_validate_password = User.query.filter_by(password=password).first()
        query_validate_email = User.query.filter_by(email=email).first()

        if username == password:
            uri_parameters = 'invalid'
            flash('Username and Password are very same', 'danger')
            return redirect(url_for('register', error=uri_parameters))
        elif query_validate_username is not None or query_validate_password is not None or query_validate_email is not None:
            uri_parameters = 'invalid'
            flash('That dates in use', 'danger')
            return redirect(url_for('register', error=uri_parameters))
        else:
            user_new = User(username=username, password=password, email=email)
            db.session.add(user_new)
            db.session.commit()
            db.session.add(user_new.follow(user_new))
            db.session.commit()
            flash('Your user commit!', 'success')
            return redirect(url_for('login'))
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
            session['username'] = username
            user_id = db.session.query(User.id).filter(User.username == session['username']).first()
            session['id'] = user_id[0]
            session['email'] = user.email

            flash('Bienvenido {}'.format(username), 'success')
            return redirect(url_for('user', username=username))

        else:
            flash('Username or password invalid', 'danger')
            return redirect(url_for('login', ))

    return render_template('sign/login.html', form=new_Loginform)


@app.route('/logout')
@user_required
def logout():
    session.clear()
    return redirect(url_for('login'))


# User Information Form and More Things ----------------------------------------------

@app.route('/setting/personal_info', methods=['GET', 'POST'])
@user_required
def setting_personal():
    new_PersonalForm = PersonalForm(request.form)
    Personal_info = Personal_User.query.filter_by(id_user=session['id']).one_or_none()
    if request.method == 'POST' and new_PersonalForm.validate():
        id_user = session['id']
        name = new_PersonalForm.name.data
        last_name = new_PersonalForm.last_name.data
        sex = new_PersonalForm.sex.data
        country = new_PersonalForm.country.data
        dob = new_PersonalForm.dob.data
        repository = new_PersonalForm.repository.data
        social_red = new_PersonalForm.social_red.data
        setting_new = Personal_User(id_user, name, last_name, sex,
                                    country, dob,
                                    repository, social_red)
        if Personal_info is None:
            print 'NO HAY INFO, CREAMOS LA INFO'
            db.session.add(setting_new)
            db.session.commit()
            flash('Personal date created', 'success')
            return redirect(url_for('user', username=session['username']))
        else:
            print 'SI HAY DATOS PERSONALES, ELIMINAMOS LOS VIEJOS AGREGAMOS LOS NUEVOS '
            db.session.delete(Personal_info)
            db.session.add(setting_new)
            db.session.commit()
            flash('Personal date update', 'success')
            return redirect(url_for('user', username=session['username']))

    return render_template('user/setting/form_personal.html',
                           form=new_PersonalForm, PersonalDate=Personal_info)


@app.route('/setting/curriculum_info', methods=['GET', 'POST'])
@user_required
def setting_curriculum():
    new_CurriculumForm = CurriculumForm(request.form)
    Curriculum_info = Curriculum_User.query.filter_by(id_user=session['id']).one_or_none()
    if request.method == 'POST' and new_CurriculumForm.validate():
        tittle = new_CurriculumForm.tittle.data
        university = new_CurriculumForm.university.data
        description = new_CurriculumForm.description.data
        setting_new = Curriculum_User(session['id'], tittle,
                                      university, description)
        if Curriculum_info is None:
            db.session.add(setting_new)
            db.session.commit()
            flash('Your curriculum created', 'success')
            return redirect(url_for('user', username=session['username']))
        else:
            db.session.delete(Curriculum_info)
            db.session.add(setting_new)
            db.session.commit()
            flash('Your curriculum date update', 'success')
            return redirect(url_for('user', username=session['username']))
    return render_template('user/setting/form_curriculum_user.html',
                           form=new_CurriculumForm, CurriculumDate=Curriculum_info)


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
    new_QuestionForm = QuestionForm(request.form)  # EDIT QUESTION
    new_answer_form = AnswerForm(request.form)  # FORM ANSWER
    question_data = db.session.query(Question).filter(Question.id == id).first()  # QUESTION
    User_data = User.query.filter_by(id=question_data.id_user).first()  # USER
    Tag_data = TagQuestion.query.filter_by(id_question=question_data.id).first()  # TAG
    all_Answers = AnswerLong.query.filter_by(id_question=id).all()  # ALL ANSWERS

    lang = know_mode_exist(Tag_data.tag_one, Tag_data.tag_two, Tag_data.tag_three)  # Check if exist lang

    try:
        if request.method == 'GET' and (session['id'] == User_data.id):
            return render_template('questions/question.html',
                                   Answers=all_Answers,
                                   User=User_data,
                                   Question_data=question_data,
                                   Tag=Tag_data,
                                   lang=lang,
                                   new_QuestionForm=new_QuestionForm,
                                   CRUD=True)
    except KeyError:
        pass

    if request.method == 'POST' and new_answer_form.validate():
        id_question = question_data.id
        answer_text = new_answer_form.answer_long.data
        answer_code = new_answer_form.text_area.data
        answer_new = AnswerLong(session['id'], session['username'],
                                id_question, answer_text, answer_code)

        db.session.add(answer_new)
        db.session.commit()
        flash('New answer!', 'success')
        return redirect(url_for('questions', id=id))

    return render_template('questions/question.html',
                           Answers=all_Answers,
                           answer_long=new_answer_form,
                           new_QuestionForm=new_QuestionForm,
                           User=User_data,
                           Question_data=question_data,
                           Tag=Tag_data,
                           lang=lang,
                           CRUD=False,
                           is_authenticated=True if 'username' in session else False)




# row will be deleted from the "secondary" table
# automatically
#myparent.children.remove(somechild)


@user_required
@csrf.exempt
@app.route('/upvote/<string:model>/id/<int:id>', methods=['GET', 'POST'])
def upvote(model, id):
    print model
    if request.method == "POST":
        if model == 'question':

            query_model = Question.query.filter_by(id=id).first()
            user_in_query_upvote = Upvote.query.filter(Upvote.users_upvote.
                                                       any(id_user=session['id'])).one_or_none()

            if query_model.upvote_count == 0 or user_in_query_upvote == None:
                query_model.upvote.append(Upvote(id_user=session['id']))
                db.session.commit()
            else:
                query_model.upvote_count -= 1
                db.session.delete(user_in_query_upvote)
                db.session.commit()
                db.session.refresh(query_model)

        elif model == 'answer':
            query_model = AnswerLong.query.filter_by(id=id).first()
            user_in_query_upvote = Answer_Upvote.query.filter(Answer_Upvote.users_answer_upvote.
                                                        any(id_user=session['id'])).one_or_none()

            if query_model.upvote_count == 0 or user_in_query_upvote == None:
                query_model.upvote.append(Answer_Upvote(id_user=session['id']))
                db.session.commit()
            else:
                query_model.upvote_count -= 1
                db.session.delete(user_in_query_upvote)
                db.session.commit()
                db.session.refresh(query_model)

        return json.dumps({'status': 'OK', 'likes': query_model.upvote_count})


@user_required
@csrf.exempt
@app.route('/downvote/<string:model>/id/<int:id>', methods=['GET', 'POST'])
def downvote(model, id):
    print model
    if request.method == "POST":
        if model == 'question':

            query_model = Question.query.filter_by(id=id).first()
            user_in_query_downvote = Downvote.query.filter(Downvote.users_downvote.
                                                       any(id_user=session['id'])).one_or_none()

            if query_model.downvote_count == 0 or user_in_query_downvote == None:
                query_model.downvote.append(Downvote(id_user=session['id']))
                db.session.commit()
            else:
                query_model.downvote_count -= 1
                db.session.delete(user_in_query_downvote)
                db.session.commit()
                db.session.refresh(query_model)

        elif model == 'answer':
            query_model = AnswerLong.query.filter_by(id=id).first()
            user_in_query_downvote = Answer_Downvote.query.filter(Answer_Downvote.users_answer_downvote.
                                                        any(id_user=session['id'])).one_or_none()

            if query_model.downvote_count == 0 or user_in_query_downvote == None:
                query_model.downvote.append(Answer_Downvote(id_user=session['id']))
                db.session.commit()
            else:
                query_model.downvote_count -= 1
                db.session.delete(user_in_query_downvote)
                db.session.commit()
                db.session.refresh(query_model)

        return json.dumps({'status': 'OK', 'likes': query_model.downvote_count})


@app.route('/questions/write/user/<string:username>', methods=['GET', 'POST'])
@user_required
def create_question(username):
    username = session['username']
    new_QuestionForm = QuestionForm(request.form)
    if request.method == 'POST' and new_QuestionForm.validate():
        query = db.session.query(User.id).filter(User.username == session['username']).first()
        user_id = query[0]  # long integer delete 'L'
        title = new_QuestionForm.tittle.data
        description = new_QuestionForm.description.data
        text_area = new_QuestionForm.text_area.data
        question_new = Question(user_id, title, description, text_area)

        db.session.add(question_new)

        id_question = db.session.query(Question.id).filter(Question.id_user == session['id'],
                                                           Question.title == title).first()
        id_question_for_tag = id_question[0]
        tag_new = TagQuestion(id_question_for_tag, new_QuestionForm.tag_one.data, new_QuestionForm.tag_two.data,
                              new_QuestionForm.tag_three.data)
        db.session.add(tag_new)
        db.session.commit()
        flash('Perfect', 'info')
        id = db.session.query(Question.id).filter(Question.id_user == session['id'], Question.title == title).first()
        return redirect(url_for('questions', id=id[0]))
    return render_template('questions/create_question.html', form=new_QuestionForm)


@app.route('/questions/edit/id/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    QuestionQuerySet = Question.query.filter_by(id=id).one_or_none()
    edited_QuestionForm = QuestionForm(request.form)
    new = [edited_QuestionForm.tittle.data, edited_QuestionForm.description.data, edited_QuestionForm.text_area.data]
    old = [QuestionQuerySet.title, QuestionQuerySet.description, QuestionQuerySet.text_area]

    new = [i for i in new if i.isspace() != True and i != '']  # CHECK EMPTY STRING AND DELETE

    if request.method == 'POST' and len(new) == 3 and set(new) != set(old):
        if (new[0] != QuestionQuerySet.title):
            QuestionQuerySet.title = new[0]
            db.session.add(QuestionQuerySet)
            db.session.commit()
        if (new[1] != QuestionQuerySet.description):
            QuestionQuerySet.description = new[1]
            db.session.add(QuestionQuerySet)
            db.session.commit()
        if (new[2] != QuestionQuerySet.text_area):
            QuestionQuerySet.text_area = new[2]
            db.session.add(QuestionQuerySet)
            db.session.commit()
        flash('Edit ready!', 'success')
        return redirect(url_for('questions', id=id))
    elif len(new) < 3:
        flash('Wow...! Olvidaste algun campo?', 'danger')
        return redirect(url_for('questions', id=id))
    else:
        flash('Wow...! Seguro hiciste algun cambio?', 'danger')
        return redirect(url_for('questions', id=id))


@app.route('/questions/delete/id/<int:id>', methods=['GET', 'POST'])
def delete_question(id):
    delete_Question = db.session.query(Question).filter(Question.id == id).first()
    db.session.delete(delete_Question)
    db.session.commit()
    return redirect(url_for('user', username=session['username']))


# Snippets ---------------------------------------------------------------------


@app.route('/snippets', methods=['GET', 'POST'])
@app.route('/snippets/page/<int:page>', methods=['GET', 'POST'])
def snippets_pagination(page=1):
    query_snippets = Snippet.query.paginate(page, 3, False)
    for date in query_snippets.items:
        date.create_date = str(date.create_date).split(" ")[0]
    return render_template('snippets/snippets_pagination.html',
                           snippets=query_snippets)


@app.route('/snippets/id/<int:id>', methods=['GET', 'POST'])
def snippets(id):
    new_SnippetForm = SnippetsForm(request.form)  # FORM SNIPPET
    new_comment_form = SnippetsComment(request.form)  # FORM COMMENT
    snippet_data = db.session.query(Snippet).filter(Snippet.id == id).first()  # SNIPPET
    User_data = User.query.filter_by(id=snippet_data.id_user).first()  # USER
    Tag_data = TagSnippet.query.filter_by(id_snippet=snippet_data.id).first()  # TAG
    create_date = str(snippet_data.create_date).split(" ")[0]  # DATE FORMATE
    lang = know_lang(know_file_extension(snippet_data.title))

    try:
        if request.method == 'GET' and session['id'] == User_data.id:
            all_Comments = CommentSnippet.query.filter_by(id_snippet=id).all()  # ALL COMMENT
            return render_template('snippets/snippet.html',
                                   Comments=all_Comments,
                                   User=User_data,
                                   Snippet_data=snippet_data,
                                   Tag=Tag_data,
                                   lang=lang,
                                   create_date=create_date,
                                   new_SnippetForm=new_SnippetForm,
                                   CRUD=True)
    except KeyError:
        pass

    if request.method == 'POST' and new_comment_form.validate():
        id_snippets = snippet_data.id
        comment_text = new_comment_form.comment.data
        comment_new = CommentSnippet(session['id'], id_snippets,
                                     session['username'],
                                     comment_text.upper())

        db.session.add(comment_new)
        db.session.commit()
        flash('New comment!', 'success')
        return redirect(url_for('snippets', id=id))

    all_Comments = CommentSnippet.query.filter_by(id_snippet=id).all()  # ALL COMMENT
    return render_template('snippets/snippet.html',
                           Comments=all_Comments,
                           comment_form=new_comment_form,
                           User=User_data,
                           Snippet_data=snippet_data,
                           Tag=Tag_data,
                           lang=lang,
                           create_date=create_date,
                           new_SnippetForm=new_SnippetForm,
                           CRUD=False,
                           is_authenticated=True if 'username' in session else False)


@app.route('/snippets/edit/id/<int:id>', methods=['GET', 'POST'])
def edit_snippet(id):
    SnippetQuerySet = Snippet.query.filter_by(id=id).one_or_none()
    edited_SnippetForm = SnippetsForm(request.form)
    new = [edited_SnippetForm.tittle.data, edited_SnippetForm.description.data, edited_SnippetForm.text_area.data]
    old = [SnippetQuerySet.title, SnippetQuerySet.description, SnippetQuerySet.text_area]

    new = [i for i in new if i.isspace() != True and i != '']  # CHECK EMPTY STRING AND DELETE

    if request.method == 'POST' and len(new) == 3 and set(new) != set(old):
        if (new[0] != SnippetQuerySet.title):
            SnippetQuerySet.title = new[0]
            db.session.add(SnippetQuerySet)
            db.session.commit()
        if (new[1] != SnippetQuerySet.description):
            SnippetQuerySet.description = new[1]
            db.session.add(SnippetQuerySet)
            db.session.commit()
        if (new[2] != SnippetQuerySet.text_area):
            SnippetQuerySet.text_area = new[2]
            db.session.add(SnippetQuerySet)
            db.session.commit()
        flash('Edit ready!', 'success')
        return redirect(url_for('snippets', id=id))
    elif len(new) < 3:
        flash('Wow...! Olvidaste algun campo?', 'danger')
        return redirect(url_for('snippets', id=id))
    else:
        flash('Wow...! Seguro hiciste algun cambio?', 'danger')
        return redirect(url_for('snippets', id=id))


@app.route('/snippets/write/user/<string:username>', methods=['GET', 'POST'])
def create_snippet(username):
    username = session['username']
    new_SnippetForm = SnippetsForm(request.form)
    if request.method == 'POST' and new_SnippetForm.validate():
        query = db.session.query(User.id).filter(User.username == session['username']).first()
        user_id = query[0]
        title = new_SnippetForm.tittle.data
        description = new_SnippetForm.description.data
        text_area = new_SnippetForm.text_area.data
        snippet_new = Snippet(user_id, title, description, text_area)

        db.session.add(snippet_new)

        id_snippet = db.session.query(Snippet.id).filter(Snippet.id_user == session['id'],
                                                         Snippet.title == title).first()
        id_snippet_for_tag = id_snippet[0]
        tag_new = TagSnippet(id_snippet_for_tag, new_SnippetForm.tag_one.data, new_SnippetForm.tag_two.data,
                             new_SnippetForm.tag_three.data)
        db.session.add(tag_new)
        db.session.commit()
        flash('Perfect', 'info')
        id = db.session.query(Snippet.id).filter(Snippet.id_user == session['id'], Snippet.title == title).first()
        return redirect(url_for('snippets', id=id[0]))
    return render_template('snippets/create_snippet.html', form=new_SnippetForm)


@app.route('/snippets/delete/id/<int:id>', methods=['GET', 'POST'])
def delete_snippet(id):
    delete_Snippet = db.session.query(Snippet).filter(Snippet.id == id).first()
    db.session.delete(delete_Snippet)
    db.session.commit()
    return redirect(url_for('user', username=session['username']))

@user_required
@csrf.exempt
@app.route('/star/<int:id>', methods=['GET', 'POST'])
def star(id):
    if request.method == "POST":
        UserSession = User.query.filter_by(username=session['username']).first()
        QuerySnippet = Snippet.query.filter_by(id=id).first()
        user_in_query_star = Star.query.filter(Star.users_snippet_star.any(id_user=UserSession.id)).one_or_none()

        if user_in_query_star == None:
            QuerySnippet.star.append(Star(id_user=session['id']))
            db.session.commit()
        else:
            QuerySnippet.star_count -= 1
            db.session.commit()
            db.session.refresh(QuerySnippet)
        return json.dumps({'status': 'OK', 'likes': QuerySnippet.star_count})


# Follow functionality ---------------------------------------------------------

@app.route('/follow/<username>')
@user_required
def follow(username):
    UserSession = User.query.filter_by(username=session['username']).first()
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username,  'danger')
        return redirect(url_for('index'))
    if user.id == UserSession.id:
        flash('You can\'t follow yourself!',  'danger')
        return redirect(url_for('user', username=username))
    u = UserSession.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '.',  'danger')
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!',  'success')
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@user_required
def unfollow(username):
    UserSession = User.query.filter_by(username=session['username']).first()
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username,  'danger')
        return redirect(url_for('index'))
    if user.id == UserSession.id:
        flash('You can\'t unfollow yourself!',  'danger')
        return redirect(url_for('user', username=username))
    u = UserSession.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + username + '.',  'danger')
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.',  'success')
    return redirect(url_for('user', username=username))

# Query Debbuging  -------------------------------------------------------------

@app.route('/query/question')
def query_question():
    cur = mysql.connection.cursor()
    cur.execute('Select a.title, a.create_date from user_question as a,\
                user as b where a.id_user = 1 and b.id = 1 order by a.create_date limit 5')
    rv = cur.fetchall()
    return jsonify(questions=rv)

