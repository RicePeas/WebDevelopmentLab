from flask_login import logout_user, current_user, login_user, login_required
from app import app, tasks, posts, db
from app.forms import FormLogin, RegistrationForm
from flask import abort, jsonify, request, make_response
from flask import render_template, url_for, redirect, flash
from flask_httpauth import HTTPBasicAuth
from app.models import User, Task
from werkzeug.urls import url_parse

auth = HTTPBasicAuth()
defaultTask = '/todo/api/v.1.0/tasks'
defaultPost = '/todo/api/v.1.0/posts'


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    hmmm = Task.query.filter_by(user_id=current_user.id)

    return render_template('index.html', title='Home', user=user, taskLst=hmmm)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth.get_password
def get_password(username):
    if username == 'Zachary':
        return 'password'
    return None


@auth.error_handler
def unauthorised():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', test=form)


@app.route(defaultPost, methods=['GET'])
@auth.login_required()
def get_posts():
    return jsonify({'posts': posts})


@app.route(defaultTask, methods=['GET'])
@auth.login_required()
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/register', methods=['GET', 'POST'])
def register():
    #if current_user.is_authenticated:
    #    return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have created a new user. WELL DONE')
        return redirect((url_for('login')))
    return render_template('registration.html', title='registration', test=form)


@app.route(defaultTask, methods=['POST'])
@auth.login_required()
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }

    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route(defaultTask + '/<int:task_id>', methods=['GET'])
@auth.login_required()
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)

    return jsonify({'task': task[0]})


@app.route(defaultTask + '/<int:task_id>', methods=['PUT'])
@auth.login_required()
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not str:
        abort(400)

    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('title', task[0]['description'])
    task[0]['done'] = request.json.get('title', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route(defaultTask + '/<int:task_id>', methods=['DELETE'])
@auth.login_required()
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]

    if not task:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})