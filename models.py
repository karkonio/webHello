from peewee import CharField, IntegerField, Model, SqliteDatabase, ForeignKeyField


db = SqliteDatabase('db.sql')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField()
    password = CharField()


class Item(BaseModel):
    name = CharField()
    quantity = IntegerField()


class Customer(BaseModel):
    name = CharField()
    age = IntegerField()


class Cart(BaseModel):
    customer = ForeignKeyField(Customer, backref='carts')


class CartItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='items')
    item = ForeignKeyField(Item, backref='carts')
