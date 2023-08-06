from typing import Optional
from dataclasses import dataclass
from peewee import AutoField, TextField, IntegerField, DataError, IntegrityError

from scraper.db.models.base import BaseModel, db
import requests


class DomainModel(BaseModel):
    id = AutoField()
    domain = TextField(unique=True)
    status_code = IntegerField()

    class Meta:
        table_name = "domains"

    @classmethod
    @db.atomic()
    def add(cls, domain: str, status_code: int) -> Optional[int]:
        try:
            record_id = cls.insert(domain=domain, status_code=status_code).execute()
            return record_id
        except IntegrityError as e:
            print(e)
        except requests.exceptions.ConnectionError as e:
            print(e)

    @classmethod
    @db.atomic()
    def remove(cls, id: int):
        try:
            cls.delete().where(DomainModel.id == id).execute()
        except Exception as e:
            print(e)

    @classmethod
    @db.atomic()
    def get_data(cls):
        query = DomainModel.select().order_by(DomainModel.id.asc()).tuples()
        return query

    @classmethod
    @db.atomic()
    def amount_of_data(cls) -> Optional[int]:
        amount = DomainModel.select().count()

        return amount


if __name__ == '__main__':
    print(type(DomainModel.get_data()))