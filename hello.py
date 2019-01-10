import json
from flask import Flask
from flask import render_template
from flask import request

from models import Item

app = Flask(__name__)


@app.route('/')
def index():
    """
    Return index page of the web app
    """
    return render_template('index.html')


@app.route('/items', methods=['GET', 'POST'])
def items():
    """
    Returns items page
    """
    items = Item.get_all()
    return render_template('items.html', items=items)
