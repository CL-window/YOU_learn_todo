from flask import Blueprint
from flask import jsonify

json_view = Blueprint('json', __name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@json_view.route('/showAll', methods=['GET', 'POST'])
def show_all():
    return jsonify({'tasks': tasks})

@json_view.route('/<page>', methods=['GET', 'POST'])
def show_page(page):
    try:
        p = int(page)
    except Exception:
        print(Exception)
        p = -1

    if(p >0 and p < len(tasks) -1):
        return jsonify({'tasks': tasks[p]})
    else:
        return "index error!"