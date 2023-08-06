import os


class SmartProjectPathSensor:
    project_dir_patterns = [
        "assets",
        "node_modules",
        "packages",
        "settings",
        "table",
        "ui",
    ]

    def __init__(self, input_dir):
        self.input_dir = input_dir

    def smart_get_project_dir(self):
        for dir_path in self._traverse_dirs():
            if self._is_project_dir(dir_path):
                return dir_path
        return None

    def _traverse_dirs(self):
        dir_path = self.input_dir
        while dir_path:
            yield dir_path
            dir_path_parent = os.path.dirname(dir_path)
            if dir_path_parent == dir_path:
                break
            dir_path = dir_path_parent

    def _is_project_dir(self, dir_path):
        if not os.path.isdir(dir_path):
            return False
        for pattern in self.project_dir_patterns:
            pattern_path = os.path.join(dir_path, pattern)
            if not os.path.exists(pattern_path):
                return False
        return True
