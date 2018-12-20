import json
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)


@app.route('/')
def index():
    """
    Return index page of the web app
    """
    return render_template('index.html')


def is_key_item(key):
    if 'quantity' in key:
        return False
    if 'delete' in key:
        return False
    if key == 'add':
        return False
    return True


@app.route('/items', methods=['GET', 'POST'])
def items():
    """
    Returns items page
    Loads data from db.txt as json
    """
    with open('db.txt', 'r') as f:
        items = json.load(f)
        if request.method == 'POST':
            if 'add' in request.form:
                items['_'] = 0
            else:
                items = {}
            for key in request.form:
                print(key)
                if is_key_item(key):
                    item = request.form[key]
                    quantity_key = key + '_quantity'
                    quantity = request.form[quantity_key]
                    items[item] = int(quantity)
            for key in request.form:
                if key.endswith('delete'):
                    if request.form[key]:
                        key = key[:-7]
                        del items[key]
            with open('db.txt', 'w') as f:
                json.dump(items, f)
        return render_template('items.html', items=items)
