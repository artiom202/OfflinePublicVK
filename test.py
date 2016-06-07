from peewee import *

db = SqliteDatabase('content.db')


class ost(Model):
    text = TextField()
    pic_id = IntegerField()
    id = IntegerField()

    class Meta:
        database = db
st = ost.create(text='123', pic_id=1, id=1)
