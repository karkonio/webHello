from flask import abort, redirect, url_for, request
from flask_admin.contrib.peewee import ModelView
from flask_security import current_user
from peewee import (
    Model, SqliteDatabase,
    CharField, IntegerField, ForeignKeyField, BooleanField
)
from flask_security import UserMixin


db = SqliteDatabase('db.sql')


class BaseModel(Model):
    class Meta:
        database = db


class Role(BaseModel):
    name = CharField(unique=True)
    description = CharField()


class User(BaseModel, UserMixin):
    email = CharField()
    password = CharField()
    active = BooleanField(default=True)


class UserRoles(BaseModel):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, backref='roles')
    role = ForeignKeyField(Role, backref='users')


class Item(BaseModel):
    name = CharField()
    quantity = IntegerField()

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = CharField()
    age = IntegerField()

    def __str__(self):
        return self.name


class Cart(BaseModel):
    customer = ForeignKeyField(Customer, backref='carts')

    def __str__(self):
        return 'Cart {}'.format(self.id)


class CartItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='items')
    item = ForeignKeyField(Item, backref='carts')


class AuthMixin:
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(
                    url_for(
                        'security.login',
                        next=request.url
                    )
                )


class UserAdmin(AuthMixin, ModelView):
    pass


class ItemAdmin(AuthMixin, ModelView):
    pass


class CustomerAdmin(AuthMixin, ModelView):
    pass


class CartAdmin(AuthMixin, ModelView):
    pass


class CartItemAdmin(AuthMixin, ModelView):
    pass
