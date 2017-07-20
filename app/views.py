# coding=utf-8
from . import app, user_datastore
from flask import request, render_template, flash, json
from form import *
from models import *
from decorator_and_utils import *
from sqlalchemy import desc
from flask_security import utils, login_required, current_user


@app.before_first_request
def before_first_request():
    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    # Create two Users for testing purposes -- unless they already exists.
    encrypted_password = utils.encrypt_password('password')
    if not user_datastore.get_user('someone@example.com'):
        user_datastore.create_user(username='kathorq',
                                   password=encrypted_password,
                                   email='someone@example.com')
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(username='carlosjazz',
                                   password=encrypted_password,
                                   email='admin@example.com')

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('someone@example.com', 'end-user')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index')), 404 # No found


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        UserDate = User.query.filter_by(username=current_user.username).first()
    Questions = UserDate.followed_question().limit(5) if current_user.is_authenticated \
                    else exec_query('SELECT * FROM user_question ORDER BY user_question.create_date DESC LIMIT 5')
    Answers = UserDate.followed_answer().limit(5) if current_user.is_authenticated \
                    else exec_query('SELECT * FROM user_answer_long ORDER BY user_answer_long.create_date DESC LIMIT 5')
    Snippets = UserDate.followed_snippet().limit(5) if current_user.is_authenticated \
                    else exec_query('SELECT * FROM user_snippet ORDER BY user_snippet.create_date DESC LIMIT 5')

    return render_template('index.html',
                            Questions=Questions,
                            Answers=Answers,
                            Snippets=Snippets,
                            username=current_user.username if current_user.is_authenticated else 'Friend')

                          
@app.route('/user/<string:username>', methods=['GET', 'POST'])
def user(username):
    UserDate = User.query.filter_by(username=username).first()
    PersonalDate = Personal_User.query.filter_by(id_user=UserDate.id).first()
    CurriculumDate = Curriculum_User.query.filter_by(id_user=UserDate.id).first()
    QuerySkill = db.session.query(Skill.skill_name).filter_by(user_id=UserDate.id).all()

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
        if request.method == 'GET' and current_user.id == UserDate.id:
            return render_template('user/user.html',
                                   user_link=user_link,
                                   PersonalDate=PersonalDate,
                                   country=country,
                                   UserDate=UserDate,
                                   Questions=Questions,
                                   Snippets=Snippets,
                                   Answers=Answers,
                                   CurriculumDate=CurriculumDate,
                                   QuerySkill=QuerySkill if QuerySkill is not None else [],
                                   CRUD=True)
    except AttributeError:
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
                           QuerySkill=QuerySkill if QuerySkill is not None else [],
                           CRUD=False,
                           is_authenticated=True if current_user.is_authenticated else False) #BUG


@app.route('/setting/personal_info', methods=['GET', 'POST'])
@login_required
def setting_personal():
    model = Personal_User.query.filter_by(id_user=current_user.id).one_or_none()

    form = PersonalForm(request.form)

    if request.method == 'POST':
        if form.validate(model):
            flash('Personal information update', 'success')
            return redirect(url_for('user', username=current_user.username))
        else:
            flash('Any field empty?', 'danger')

    return render_template('user/setting/form_personal.html',
                           form=form, PersonalDate=model)


@app.route('/setting/curriculum_info', methods=['GET', 'POST'])
@login_required
def setting_curriculum():
    form = CurriculumForm(request.form)
    model = Curriculum_User.query.filter_by(id_user=current_user.id).one_or_none()
    skills = Skill.query.filter_by(user_id=current_user.id)

    if request.method == 'POST':
        if form.validate(model):
            flash('Curriculum information update', 'success')
            return redirect(url_for('user', username=current_user.username))
        else:
            flash('Any field empty?', 'danger')

    return render_template('user/setting/form_curriculum_user.html',
                           form=form,
                           CurriculumDate=model,
                           SkillDate=skills,
                           formskill=SkillForm())


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

    for answer in all_Answers:
        answer.create_date = str(answer.create_date).split(" ")[0]
        
    lang = know_mode_exist(Tag_data.tag_one, Tag_data.tag_two, Tag_data.tag_three)  # Check if exist lang

    if current_user.is_authenticated:
        if request.method == 'GET' and current_user.id == User_data.id:
            return render_template('questions/question.html',
                                   Answers=all_Answers,
                                   User=User_data,
                                   Question_data=question_data,
                                   Tag=Tag_data,
                                   lang=lang,
                                   new_QuestionForm=new_QuestionForm,
                                   CRUD=True)

    if request.method == 'POST' and new_answer_form.validate():
        id_question = question_data.id
        answer_text = new_answer_form.answer_long.data
        answer_code = new_answer_form.text_area.data
        answer_new = AnswerLong(current_user.id,
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
                           is_authenticated=True if current_user.is_authenticated else False)


@app.route('/upvote', methods=['GET'])
def upvote():
    double_click = False # Flow control, if there is already a like of the user then no other like

    if request.method == "GET":

        id = request.args.get('id')
        model = request.args.get('model')

        if model == 'question':
            query_model = Question.query.filter_by(id=id).first()
        elif model == 'answer':
            query_model = AnswerLong.query.filter_by(id=id).first()

        for record in query_model.upvote:
            if record.id_user == current_user.id:
                query_model.upvote.remove(record)
                db.session.commit()

                double_click = True

        if not double_click:
            if isinstance(query_model, AnswerLong):
                query_model.upvote.append(Answer_Upvote(id_user=current_user.id))
            elif isinstance(query_model, Question):
                query_model.upvote.append(Upvote(id_user=current_user.id))

            db.session.commit()

        return json.dumps({'status': 'OK', 'likes': query_model.upvote_count})

@app.route('/downvote', methods=['GET'])
def downvote():
    double_click = False # Flow control, if there is already a like of the user then no other like

    if request.method == "GET":

        id = request.args.get('id')
        model = request.args.get('model')

        if model == 'question':
            query_model = Question.query.filter_by(id=id).first()
        elif model == 'answer':
            query_model = AnswerLong.query.filter_by(id=id).first()

        for record in query_model.downvote:
            if record.id_user == current_user.id:
                query_model.downvote.remove(record)
                db.session.commit()

                double_click = True

        if not double_click:
            if isinstance(query_model, AnswerLong):
                query_model.downvote.append(Answer_Downvote(id_user=current_user.id))
            elif isinstance(query_model, Question):
                query_model.downvote.append(Downvote(id_user=current_user.id))

            db.session.commit()

        return json.dumps({'status': 'OK', 'likes': query_model.downvote_count})


@app.route('/questions/write/user/<string:username>', methods=['GET', 'POST'])
@login_required
def create_question(username):
    new_QuestionForm = QuestionForm(request.form)
    if request.method == 'POST' and new_QuestionForm.validate():
        list_tags = [new_QuestionForm.tag_one.data, new_QuestionForm.tag_two.data, new_QuestionForm.tag_three.data]

        if len(list_tags) > len(set(list_tags)):
            flash('Tags must be different', 'danger')
            return render_template('questions/create_question.html', form=new_QuestionForm)

        title = new_QuestionForm.tittle.data
        description = new_QuestionForm.description.data
        text_area = new_QuestionForm.text_area.data

        question_new = Question(current_user.id, title, description, text_area)

        db.session.add(question_new)
        db.session.commit()

        tag_new = TagQuestion(question_new.id, list_tags[0], list_tags[1], list_tags[2])

        db.session.add(tag_new)
        db.session.commit()

        flash('Perfect', 'info')

        return redirect(url_for('questions', id=question_new.id))
    return render_template('questions/create_question.html', form=new_QuestionForm)


@app.route('/questions/edit/id/<int:id>', methods=['GET', 'POST'])
@login_required
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
        flash('Forgot a field?', 'danger')
        return redirect(url_for('questions', id=id))
    else:
        flash('Are you sure you made any changes?', 'danger')
        return redirect(url_for('questions', id=id))


@app.route('/questions/delete/id/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_question(id):
    delete_Question = db.session.query(Question).filter(Question.id == id).first()
    db.session.delete(delete_Question)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('user', username=current_user.username))


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

    if current_user.is_authenticated:
        if request.method == 'GET' and current_user.id == User_data.id:
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

    if request.method == 'POST' and new_comment_form.validate():
        comment_text = new_comment_form.comment.data
        comment_new = CommentSnippet(current_user.id, snippet_data.id,
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
                           is_authenticated=True if current_user.is_authenticated else False)


@app.route('/snippets/edit/id/<int:id>', methods=['GET', 'POST'])
@login_required
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
        flash('Forgot a field?', 'danger')
        return redirect(url_for('snippets', id=id))
    else:
        flash('Are you sure you made any changes?', 'danger')
        return redirect(url_for('snippets', id=id))


@app.route('/snippets/write/user/<string:username>', methods=['GET', 'POST'])
@login_required
def create_snippet(username):
    new_SnippetForm = SnippetsForm(request.form)
    if request.method == 'POST' and new_SnippetForm.validate():
        title = new_SnippetForm.tittle.data
        description = new_SnippetForm.description.data
        text_area = new_SnippetForm.text_area.data
        snippet_new = Snippet(current_user.id, title, description, text_area)
        list_tags = [new_SnippetForm.tag_one.data, new_SnippetForm.tag_two.data, new_SnippetForm.tag_three.data]
        
        if len(list_tags) > len(set(list_tags)):
            flash('Tags must be different', 'danger')
            return render_template('snippets/create_snippet.html', form=new_SnippetForm)

        db.session.add(snippet_new)
        id_snippet = db.session.query(Snippet.id).filter(Snippet.id_user == current_user.id,
                                                         Snippet.title == title).first()
        tag_new = TagSnippet(id_snippet[0], list_tags[0], list_tags[1], list_tags[2] )
        db.session.add(tag_new)
        db.session.commit()
        flash('Perfect', 'info')
        id = db.session.query(Snippet.id).filter(Snippet.id_user == current_user.id, Snippet.title == title).first()
        return redirect(url_for('snippets', id=id[0]))
    return render_template('snippets/create_snippet.html', form=new_SnippetForm)


@app.route('/snippets/delete/id/<int:id>', methods=['GET', 'POST'])
def delete_snippet(id):
    delete_Snippet = db.session.query(Snippet).filter(Snippet.id == id).first()
    db.session.delete(delete_Snippet)
    db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('user', username=current_user.username))


@app.route('/star/<int:id>', methods=['GET', 'POST'])
def star(id):
    if request.method == "POST":
        double_click = False
        QuerySnippet = Snippet.query.filter_by(id=id).first()

        for record in QuerySnippet.star:
            if record.id_user == current_user.id:
                QuerySnippet.star.remove(record)
                db.session.commit()

                double_click = True

        if not double_click:
            QuerySnippet.star.append(Star(id_user=current_user.id))
            db.session.commit()

        return json.dumps({'status': 'OK', 'likes': QuerySnippet.star_count})


@app.route('/follow/<username>')
@login_required
def follow(username):
    UserSession = User.query.filter_by(id=current_user.id).first()
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
@login_required
def unfollow(username):
    UserSession = User.query.filter_by(id=current_user.id).first()
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


@app.route('/skill/id/<int:id>', methods=['GET', 'POST'])
def skill(id):
    UserSession = User.query.filter_by(id=id).first()
    if Skill.query.filter_by(user_id=id).count() == 10:
        flash("You can not have more than 10 skill", 'warning')
        return redirect(url_for('setting_curriculum'))
    form = SkillForm(request.form)
    skill = form.skill_name.data
    if request.method == 'POST' and form.validate():
        newskill = Skill(UserSession.id, skill)
        db.session.add(newskill)
        db.session.commit()
        flash("Saved Changes", 'success')
        return redirect(url_for('setting_curriculum'))
    else:
        flash("Error", 'danger')
        return redirect(url_for('setting_curriculum'))


@app.route('/skill/delete/id/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_skill(id):
    QuerySkill = Skill.query.filter_by(id=id).one_or_none()
    skillname = QuerySkill.skill_name
    if QuerySkill == None:
        flash('Error', 'warning')
    else:
        db.session.delete(QuerySkill)
        db.session.commit()
        flash('Skill %s deleted!' % skillname, 'success')
    return redirect(url_for('setting_curriculum'))


@app.route('/explorer', methods=['GET'])
def explorer():
    users = db.session.query(User).all()
    return render_template('explorer.html', users=users)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')