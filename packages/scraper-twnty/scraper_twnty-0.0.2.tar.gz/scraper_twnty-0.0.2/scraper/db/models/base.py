from playhouse.shortcuts import PostgresqlDatabase
from peewee import Model

db = PostgresqlDatabase('domains', user='domains', password='domains', host='localhost')


class BaseModel(Model):
    class Meta:
        database = db
