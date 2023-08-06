import os


class PathUtils:
    @staticmethod
    def make_sure_path_exist(input_path):
        if not os.path.exists(input_path):
            os.makedirs(input_path)

    @staticmethod
    def make_sure_path_exist_and_empty(input_path):
        if os.path.exists(input_path):
            os.remove(input_path)
        else:
            PathUtils.make_sure_path_exist(os.path.dirname(input_path))
