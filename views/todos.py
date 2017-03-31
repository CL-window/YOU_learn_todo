# coding: utf-8

from leancloud import Object
from leancloud import User
from leancloud import Query
from leancloud import ACL
from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash


class Todo(Object):
    pass

todos_view = Blueprint('todos', __name__)

TRASHED, PLANNED, COMPLETED = -1, 0, 1


# 显示所有 Todo
@todos_view.route('')
def show():
    status = int(request.args.get('status', PLANNED))
    try:
        todos = Query(Todo).add_descending('createdAt').equal_to('status', status).find()
    except LeanCloudError as e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            todos = []
        else:
            flash(e.error)
    return render_template('todos.html', todos=todos, status=status)


# 新建一个 Todo
@todos_view.route('', methods=['POST'])
def add():
    content = request.form['content']
    todo = Todo()
    todo.set('content', content)
    todo.set('status', PLANNED)
    author = User.get_current()
    if author:
        todo.set('author', author)  # 关联 todo 的作者
        acl = ACL()
        acl.set_write_access(author, True)
        acl.set_read_access(author, True)
        todo.set_acl(acl)  # 设置 ACL
    try:
        todo.save()
    except LeanCloudError as e:
        flash(e.error)
    return redirect(url_for('todos.show'))


# 删除一个 Todo
@todos_view.route('/<todo_id>', methods=['DELETE'])
def delete(todo_id):
    status = int(request.args.get('status', PLANNED))
    todo = Todo.create_without_data(todo_id)
    todo.set('status', TRASHED)
    try:
        todo.save()
    except LeanCloudError as e:
        flash(e.error)
    return redirect(url_for('todos.show', status=status))


# 将一个 Todo 的状态设置为已完成
@todos_view.route('/<todo_id>/done', methods=['POST'])
def done(todo_id):
    status = int(request.args.get('status', PLANNED))
    todo = Todo.create_without_data(todo_id)
    todo.set('status', COMPLETED)
    try:
        todo.save()
    except LeanCloudError as e:
        flash(e.error)
    return redirect(url_for('todos.show', status=status))


# 将一个 Todo 的状态设置为未完成
@todos_view.route('/<todo_id>/undone', methods=['POST'])
def undone(todo_id):
    status = int(request.args.get('status', PLANNED))
    todo = Todo.create_without_data(todo_id)
    todo.set('status', PLANNED)
    try:
        todo.save()
    except LeanCloudError as e:
        flash(e.error)
    return redirect(url_for('todos.show', status=status))