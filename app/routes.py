from flask_login import logout_user

from app import app, tasks, posts
from app.forms import Login
from flask import abort, jsonify, request, make_response
from flask import render_template, url_for, redirect, flash
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
defaultTask = '/todo/api/v.1.0/tasks'
defaultPost = '/todo/api/v.1.0/posts'



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


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me{}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/index')
@auth.login_required()
def index():
    user = {'username': 'Miguel'}
    hmmm = posts

    return render_template('index.html', title='Home', user=user, post=hmmm)


@app.route(defaultPost, methods=['GET'])
@auth.login_required()
def get_posts():
    return jsonify({'posts': posts})


@app.route(defaultTask, methods=['GET'])
@auth.login_required()
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


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