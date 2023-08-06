import os

from util.table_utils import is_file_filtered


class TableSheetFiles:
    def __init__(self):
        self.all_files = []

    def has_file(self):
        return len(self.all_files) > 0

    def read_product_files(self, file_path, dimensions):
        if not os.path.exists(file_path):
            print(f"table dir NOT exist! dir=>[{file_path}]")
            return None

        input_file_path = os.path.abspath(file_path)
        self.read_files_in_dir(input_file_path)

        for dimension in reversed(dimensions.split(',')):
            if dimension:
                self.read_files_in_dir(os.path.join(input_file_path, dimension))
        print(f"load table sheet files finish. count=>[{len(self.all_files)}]")

    def read_files_in_dir(self, dir_path):
        if not os.path.exists(dir_path):
            return

        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if not os.path.isfile(file_path) or is_file_filtered(file_path):
                continue
            self.all_files.append(file_path)

    def is_file_in_list(self, file_name):
        for file in self.all_files:
            if os.path.basename(file) == file_name:
                return True
        return False

    def get_all_files(self):
        return self.all_files
