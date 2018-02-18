import peewee
from app import app
from flask import request

banco = peewee.SqliteDatabase('banco.db')

class Climate(peewee.Model):
    date = peewee.DateField()
    rainfall = peewee.FloatField()
    temperature = peewee.IntegerField()
	
    def to_dict(self):
        return {'id':self.id, 'date': self.date, 'rainfall': self.rainfall, 'temperature': self.temperature}

    class Meta:
        database = banco
		
try:
    banco.create_table(Climate)
except Exception as e:
    pass