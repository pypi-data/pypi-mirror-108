from typing import Optional
from dataclasses import dataclass
from peewee import AutoField, TextField, DataError, IntegrityError

from scraper.db.models.base import BaseModel, db


@dataclass(frozen=True)
class LinkData:
    id: int
    domain: str


class LinkModel(BaseModel):
    id = AutoField()
    domain = TextField(unique=True)

    class Meta:
        table_name = "links"

    @classmethod
    @db.atomic()
    def add(cls, domain: str) -> Optional[int]:
        try:
            record_id = cls.insert(domain=domain).execute()
            return record_id
        except IntegrityError as e:
            print(e)

    @classmethod
    @db.atomic()
    def remove(cls, id: int):
        try:
            cls.delete().where(LinkModel.id == id).execute()
        except Exception as e:
            print(e)

    @classmethod
    @db.atomic()
    def get_data(cls):
        query = LinkModel.select().order_by(LinkModel.id.asc()).tuples()
        return query


    @classmethod
    @db.atomic()
    def amount_of_data(cls) -> Optional[int]:
        amount = LinkModel.select().count()

        return amount
