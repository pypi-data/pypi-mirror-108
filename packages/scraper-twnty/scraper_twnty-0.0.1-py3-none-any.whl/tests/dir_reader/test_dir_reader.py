from scraper.dir_reader import FileReader
import pytest
from os import path, makedirs
from shutil import rmtree
from pathlib import Path


@pytest.mark.usefixtures("test_directory")
class TestDirReader:

    def test_move_to_trash(self):
        fr = FileReader("dir_reader/in/test", "dir_reader/out/")
        fr.move_to_trash('dir_reader/in/test/test_file2.txt', 'test_file2.txt')

        assert path.exists('dir_reader/in/test/') is True
        assert path.exists('dir_reader/in/test/test_file2.txt') is False
        assert path.exists('dir_reader/out/test_file2.txt') is True

    def test_delete_empty_folders(self):
        fr = FileReader("dir_reader/in/test", "dir_reader/out/")
        fr.get_files()
        fr.delete_empty_folders("dir_reader/in/")

        assert path.exists("dir_reader/in/test") is False
        assert path.exists("dir_reader/in/test/subtest") is False
