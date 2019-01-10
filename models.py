import sqlite3


class Item:
    @classmethod
    def __execute(cls, statement):
        conn = sqlite3.connect('db.sql')
        cursor = conn.cursor()
        cursor.execute(statement)
        return cursor, conn

    @classmethod
    def get(cls, id):
        statement = 'SELECT * FROM items WHERE id={}'.format(id)
        cursor, conn = cls.__execute(statement)
        result = cursor.fetchone()
        conn.close()
        return result

    @classmethod
    def get_all(cls):
        statement = 'SELECT * FROM items'
        cursor, conn = cls.__execute(statement)
        result = cursor.fetchall()
        conn.close()
        return result
