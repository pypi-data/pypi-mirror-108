from pathlib import Path
from os import walk, listdir, rename, path, mkdir
from scraper.data_parsing.parser import Parser
from shutil import rmtree


class FileReader:
    def __init__(self, folder_root, trash_folder):
        self.folders = []
        self.folder_root = folder_root
        self.trash_folder = trash_folder

    def move_to_trash(self, abs_file_path: str, file_name: str):
        try:
            rename(abs_file_path, Path(self.trash_folder, file_name))
        except FileNotFoundError as e:
            print(str(e))

    def delete_empty_folders(self, root):
        subdirectories = listdir(root)

        for d in subdirectories:
            rmtree(root + '/' + d)

    def get_files(self):
        try:
            self.folders = []
            for i in walk(self.folder_root):
                self.folders.append(i)

            for address, dirs, files in self.folders:
                for file in files:
                    abs_fpath = address + '/' + file

                    if '.html' in file:
                        parser = Parser(abs_fpath)
                        parser.parse()
                    self.move_to_trash(abs_fpath, file)
        except TypeError as e:
            print(e)

    def run(self):
        self.get_files()
        self.delete_empty_folders(self.folder_root)
