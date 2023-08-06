from scraper.parser import Parser
from datetime import datetime
import pytest
from scraper.db.models.links_model import LinkModel
from tests.conftest import LinkRecord


def test_link_check():
    empty_str = Parser.link_check("")
    date = Parser.link_check(str(datetime.date))
    wrong_format = Parser.link_check("test://test.com/")
    right_format = Parser.link_check("http://test.test.com.ua/hello/test")
    right_format2 = Parser.link_check("https://test.com/")

    assert empty_str is False
    assert date is False
    assert wrong_format is False
    assert right_format is True
    assert right_format2 is True


def test_domain_preparing():
    domain = "test.test.test"
    link = "https://test.test.test/something"
    link2 = "http://test.test.test:gjjgkg/something"
    link3 = "http://www.test.test.test/something"
    link4 = "https://www.test.test.test"

    assert domain == Parser.domain_preparing(link)
    assert domain == Parser.domain_preparing(link2)
    assert domain == Parser.domain_preparing(link3)
    assert domain == Parser.domain_preparing(link4)


def test_parser_file_path():
    right_file_path = "tests/parser/test.txt"
    wrong_file_path = ""

    assert Parser(right_file_path).parse() is True
    assert Parser(wrong_file_path).parse() is False

