import json

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/items', methods=['GET', 'POST'])
def items():
    with open('db.txt', 'r') as f:
        items = json.load(f)
        if request.method == 'POST':
            add_item = request.form['item']
            remove_item = request.form['remove_item']
            old_item = request.form['old_item']
            change_quan = request.form['new_quan']
            if add_item:
                item = request.form['item']
                quantity = request.form['quantity']
                items.update({item: quantity})
            elif remove_item:
                del items[remove_item]
            elif old_item:
                new_item = request.form['new_item']
                items[new_item] = items[old_item]
                del items[old_item]
            elif change_quan:
                item_name = request.form['item_name']
                items[item_name] = change_quan
            with open('db.txt', 'w') as f2:
                json.dump(items, f2)
    return render_template('items.html', items=items)
# input type="hidden"
# input type="checkbox"
