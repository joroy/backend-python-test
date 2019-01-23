from alayatodo import (
    app,
    db
)


from alayatodo.models import (
    User,
    Todo,
    object_as_dict)


from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    jsonify
)


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user'] = object_as_dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = todo = Todo.query.get_or_404(id)
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    todos = Todo.query.filter_by(user_id=session['user']['id']).all()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    description = request.form.get('description', '')
    if description:
        new_todo = Todo(user_id=session['user']['id'], description=description)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo #{} has beed added'.format(new_todo.id), 'confirmation')
    else:
        flash('Description is required', 'error')
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.get_or_404(id)
    flash('Todo #{} has beed deleted'.format(todo.id), 'confirmation')
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>/mark_as_done', methods=['POST'])
def todo_mark_as_done(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.get_or_404(id)
    todo.done = request.form.get('done') == '1'
    db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>/json', methods=['GET'])
def todo_JSON(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.get_or_404(id)
    return jsonify(object_as_dict(todo))

