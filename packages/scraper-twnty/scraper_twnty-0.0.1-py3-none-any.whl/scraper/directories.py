from pathlib import Path
from os import walk, listdir, rename, path, mkdir


class Directories:
    def __init__(self, folder_root, trash_folder):
        self.folder_root = folder_root
        self.trash_folder = trash_folder

    def create_directories(self):
        if not path.exists(self.folder_root):
            mkdir(self.folder_root)
            print("Directory ", self.folder_root, " Created ")
        else:
            print("Directory ", self.trash_folder, " already exists")

        if not path.exists(self.trash_folder):
            mkdir(self.trash_folder)
            print("Directory ", self.trash_folder, " Created ")
        else:
            print("Directory ", self.trash_folder, " already exists")

    def run(self):
        self.create_directories()
