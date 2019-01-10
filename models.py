from peewee import CharField, IntegerField, Model, SqliteDatabase


db = SqliteDatabase('db.sql')


class Item(Model):
    name = CharField()
    quantity = IntegerField()

    class Meta:
        database = db
