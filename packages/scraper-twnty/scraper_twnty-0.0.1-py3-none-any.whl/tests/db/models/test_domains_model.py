from copy import copy
from datetime import datetime
from typing import Optional
from peewee import DoesNotExist, ModelSelect

import pytest

from scraper.db.models.domains_model import DomainModel
from tests.conftest import DomainRecord


class DomainAbstract:
    record: DomainRecord


@pytest.mark.usefixtures("domain_record")
class TestDomains(DomainAbstract):

    @staticmethod
    def __create_record(record: DomainRecord) -> Optional[int]:
        res = DomainModel.add(domain=record.url, status_code=record.status_code)

        return res

    def remove_all_test_records(self):
        DomainModel.delete().where(
            DomainModel.domain == self.record.url
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
        DomainModel.remove(record_id)
        self.remove_all_test_records()

        with pytest.raises(DoesNotExist):
            DomainModel.get(DomainModel.id == record_id)

    def test_get_data(self):
        assert type(DomainModel.get_data()) == ModelSelect

    def test_amount_of_data(self):
        assert type(DomainModel.amount_of_data()) == int
