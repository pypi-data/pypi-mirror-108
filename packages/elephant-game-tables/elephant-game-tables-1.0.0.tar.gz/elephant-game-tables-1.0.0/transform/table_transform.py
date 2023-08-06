import os

from template.table_transform_template import TableTransformTemplate
from transform.talbe_json_manager import TableJsonManager
from util.path_utils import PathUtils
from util.zip_utils import ZipUtils


class TableTransformManager:
    def __init__(self, prefix):
        self.ts_code_file_name_prefix = prefix
        self.table_ts_code_file_name = "TableDefines.ts"
        self.table_ts_code_manager_file_name = "TableManager.ts"
        self.table_ts_code_table_instance_file_name = "TableInstances.ts"
        self.table_json_file_name = "tables.bin"
        self.table_template = TableTransformTemplate(prefix)
        self.table_json = TableJsonManager()

    def translate(self, all_table_sheets):
        for table_name, table_sheet in all_table_sheets.items():
            self.table_json.append_table_json(table_name, table_sheet.get_contents())
            self.table_template.append_ts_code(table_name, table_sheet)

    def save_to(self, path_manager):
        self._save_ts_script_codes(path_manager.get_script_output_dir())
        self._save_json_contents(path_manager.get_json_output_dir())

    def _save_ts_script_codes(self, script_dir):
        ts_codes_output_file = os.path.join(script_dir, self._get_ts_code_file_name(self.table_ts_code_file_name))
        PathUtils.make_sure_path_exist_and_empty(ts_codes_output_file)
        with open(ts_codes_output_file, 'w', encoding='utf-8') as ts_code_file:
            content = self.table_template.get_ts_code_file_content()
            ts_code_file.write(content)
        print(f"ts code file saved! path=>[{ts_codes_output_file}]")

        ts_code_manager_output_file = os.path.join(script_dir, self._get_ts_code_file_name(self.table_ts_code_manager_file_name))
        PathUtils.make_sure_path_exist_and_empty(ts_code_manager_output_file)
        with open(ts_code_manager_output_file, 'w', encoding='utf-8') as ts_code_manager_file:
            content = self.table_template.get_ts_code_manager_file_content()
            ts_code_manager_file.write(content)
        print(f"ts code manager file saved! path=>[{ts_code_manager_output_file}]")

        ts_code_table_instances_output_file = os.path.join(script_dir, self._get_ts_code_file_name(self.table_ts_code_table_instance_file_name))
        PathUtils.make_sure_path_exist_and_empty(ts_code_table_instances_output_file)
        with open(ts_code_table_instances_output_file, 'w', encoding='utf-8') as ts_code_urls_file:
            content = self.table_template.get_ts_code_table_instances_content()
            ts_code_urls_file.write(content)
        print(f"ts code table urls file saved! path=>[{ts_code_table_instances_output_file}]")

        print("all code file are saved!")

    def _save_json_contents(self, json_dir):
        output_file = os.path.join(json_dir, self.table_json_file_name)
        PathUtils.make_sure_path_exist_and_empty(output_file)
        ZipUtils.create_zip_file(output_file, {
            self.table_json_file_name: self.table_json.get_json_contents()
        })
        print(f"json zip contents saved! path=>[{output_file}]")

    def _get_ts_code_file_name(self, file_name):
        return f'{self.ts_code_file_name_prefix}{file_name}' if self.ts_code_file_name_prefix else file_name
