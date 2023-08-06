from dataclasses import dataclass
from os import path, makedirs
from shutil import rmtree
from pathlib import Path

import pytest


@dataclass
class LinkRecord:
    url: str = "test.test.test"


@dataclass
class DomainRecord:
    url: str = "test.com.de"
    status_code = None


@pytest.fixture(scope="class")
def link_record(request):
    request.cls.record = LinkRecord()


@pytest.fixture(scope="class")
def domain_record(request):
    request.cls.record = DomainRecord()


@pytest.fixture(scope="class")
def test_directory(request):
    req = create_test_directory()
    request.cls.req = req
    yield
    remove_test_directory()


def create_test_directory():
    in_root = 'dir_reader/in/test'
    out_root = 'dir_reader/out/'

    if not path.exists(in_root):
        makedirs(in_root)
        makedirs(in_root + '/subtest')
        Path(in_root + "/subtest/test_file.txt").touch(exist_ok=True)
        Path(in_root + "/test_file2.txt").touch(exist_ok=True)

    if not path.exists(out_root):
        makedirs(out_root)


def remove_test_directory():
    if path.exists('dir_reader/in/') and path.exists('dir_reader/out/'):
        rmtree('dir_reader/in/')
        rmtree('dir_reader/out/')
