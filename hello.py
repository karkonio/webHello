import json
from flask import Flask
from flask import render_template
from flask import request, Response, session, redirect, url_for
from playhouse.shortcuts import model_to_dict, dict_to_model

from models import Item


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    """
    Return index page of the web app
    """
    name = session.get('name')
    response = render_template('index.html', name=name)
    return response


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['name'] = request.form['name']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=name>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/api/items/', methods=['GET', 'POST'])
@app.route('/api/items/<item_id>/')
def items(item_id=None):
    if request.method == 'GET':
        if item_id is not None:
            items_query = Item.select().where(Item.id == item_id)
            try:
                item = items_query[0]
                return json.dumps(model_to_dict(item))
            except IndexError:
                return Response(
                    json.dumps({'error': 'not found'}),
                    status=404
                )
        else:
            items = Item.select()
            items = [model_to_dict(item) for item in items]
            return json.dumps(items)
    elif request.method == 'POST':
        item = dict_to_model(
            data=request.json,
            model_class=Item
        )
        item.save()
        return Response(
            json.dumps(model_to_dict(item)),
            status=201
        )
