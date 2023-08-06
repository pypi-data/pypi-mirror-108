import json


class TableJsonManager:
    def __init__(self):
        self.separator = "@@$$"
        self.table_jsons = {}

    def append_table_json(self, table_name, table_json):
        self.table_jsons[table_name] = table_json

    def get_json_contents(self):
        return self.separator.join(json.dumps({table_name: table_json}, separators=(",", ":"), sort_keys=True, ensure_ascii=False) for table_name, table_json in
                                   self.table_jsons.items())
