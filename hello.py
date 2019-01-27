import json
import flask_admin
from flask import Flask
from flask import render_template
from flask import request, Response, session, redirect, url_for
from flask_security import Security, PeeweeUserDatastore, login_required
from playhouse.shortcuts import model_to_dict, dict_to_model

from models import db, User, Role, UserRoles, Item, Customer, Cart, CartItem
from admin import UserAdmin, ItemAdmin, CustomerAdmin, CartAdmin, CartItemAdmin


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'


# Setup Flask-Security
user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore)


# Setup flask-admin
admin = flask_admin.Admin(app, name='Shop Admin')
admin.add_view(UserAdmin(User))
admin.add_view(ItemAdmin(Item))
admin.add_view(CustomerAdmin(Customer))
admin.add_view(CartAdmin(Cart))
admin.add_view(CartItemAdmin(CartItem))


# Create a user to test with
@app.before_first_request
def create_user():
    for Model in (Role, User, UserRoles):
        Model.drop_table(fail_silently=True)
        Model.create_table(fail_silently=True)
    user_datastore.create_user(
        email='test@test.com',
        password='password'
    )


@app.route('/')
@login_required
def index():
    """
    Return index page of the web app
    """
    name = session.get('name')
    response = render_template('index.html', name=name)
    return response


@app.route('/api/items/', methods=['GET', 'POST'])
@app.route('/api/items/<item_id>/')
def items(item_id=None):
    if request.method == 'GET':
        if item_id is not None:
            items_query = Item.select().where(Item.id == item_id)
            try:
                item = items_query[0]
                item = json.dumps(model_to_dict(item))
                return render_template('item.html', item=item)
            except IndexError:
                return Response(
                    json.dumps({'error': 'not found'}),
                    status=404
                )
        else:
            items = Item.select()
            items = [model_to_dict(item) for item in items]
            # items = json.dumps(items)
            print(item for item in items)
            return render_template('items.html', items=items)
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
