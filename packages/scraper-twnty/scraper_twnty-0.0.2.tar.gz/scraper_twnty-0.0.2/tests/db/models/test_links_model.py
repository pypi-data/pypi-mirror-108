from copy import copy
from datetime import datetime
from typing import Optional
from peewee import DoesNotExist, ModelSelect

import pytest

from scraper.db.models.links_model import LinkModel
from tests.conftest import LinkRecord


class LinkAbstract:
    record: LinkRecord


@pytest.mark.usefixtures("link_record")
class TestLinks(LinkAbstract):

    @staticmethod
    def __create_record(record: LinkRecord) -> Optional[int]:
        res = LinkModel.add(domain=record.url)

        return res

    def remove_all_test_records(self):
        LinkModel.delete().where(
            LinkModel.domain == self.record.url
        ).execute()

    def test_add_return_value_success(self):
        self.remove_all_test_records()

        record_id = self.__create_record(self.record)

        self.remove_all_test_records()

        assert type(record_id) == int

    def test_add_unique_constraint(self):
        self.remove_all_test_records()

        record_id = self.__create_record(self.record)
        record_id2 = self.__create_record(self.record)

        self.remove_all_test_records()

        assert type(record_id) == int
        assert record_id2 is None

    def test_remove_domain(self):
        self.remove_all_test_records()

        record_id = self.__create_record(self.record)
        LinkModel.remove(record_id)
        self.remove_all_test_records()

        with pytest.raises(DoesNotExist):
            LinkModel.get(LinkModel.id == record_id)

    def test_get_data(self):
        assert type(LinkModel.get_data()) == ModelSelect

    def test_amount_of_data(self):
        assert type(LinkModel.amount_of_data()) == int
