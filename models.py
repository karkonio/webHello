from flask import abort, redirect, url_for, request
from flask_security import current_user
from peewee import (
    SqliteDatabase,
    CharField, IntegerField, ForeignKeyField, BooleanField
)
from playhouse.signals import Model, post_save
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
    manufacturer = CharField()
    price = IntegerField()

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = CharField()

    def __str__(self):
        return self.name


class Cart(BaseModel):
    customer = ForeignKeyField(Customer, backref='carts')
    paid = BooleanField(default=False)
    price = IntegerField(null=True)

    def __str__(self):
        return 'Cart {}'.format(self.id)


class CartItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='items')
    item = ForeignKeyField(Item, backref='carts')
    quantity = IntegerField()


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


@post_save(sender=CartItem)
def on_save_handler(model_class, instance, created):
    cart = instance.cart
    prices = [
        item.item.price * item.quantity for item in cart.items
    ]
    instance.cart.price = sum(prices)
    instance.cart.save()
