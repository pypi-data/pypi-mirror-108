import os


def get_relative_path(dir_path, relative_path):
    return os.path.normpath(os.path.join(dir_path, relative_path))


class BaseResourceManager:
    def __init__(self, project_root_dir, path_configs):
        self.project_root_dir = project_root_dir
        self.path_configs = path_configs

    def is_table_dir_exist(self):
        return os.path.exists(self.get_table_dir())

    def get_table_dir(self):
        return self._get_relative_path(self.path_configs["table_dir"])

    def get_script_output_dir(self):
        return self._get_relative_path(self.path_configs["script_out_dir"])

    def get_json_output_dir(self):
        return self._get_relative_path(self.path_configs["json_out_dir"])

    def _get_relative_path(self, relative_path):
        return get_relative_path(self.project_root_dir, relative_path)


class GameResourceManager(BaseResourceManager):
    def __init__(self, project_dir):
        super().__init__(project_dir, {
            "table_dir": "table",
            "script_out_dir": "assets/Script/Table",
            "json_out_dir": "assets/resources/Table"
        })


class BundleResourceManager(BaseResourceManager):
    def __init__(self, bundle_dir):
        super().__init__(bundle_dir, {
            "table_dir": ".Assets/Table",
            "script_out_dir": "Table",
            "json_out_dir": "Res/Table"
        })
