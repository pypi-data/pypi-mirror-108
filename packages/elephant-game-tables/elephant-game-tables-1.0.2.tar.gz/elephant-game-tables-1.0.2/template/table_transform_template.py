from template.table_template import TableTemplate
from template.template_context_generator import TemplateContextGenerator


class TableTransformTemplate(TableTemplate):
    def __init__(self, prefix):
        super(TableTransformTemplate, self).__init__()
        self.context_generator = TemplateContextGenerator(prefix)
        self.ts_codes = []

    def append_ts_code(self, table_name, table_sheet):
        new_ts_code = self._generate_ts_code(table_name, table_sheet)
        if new_ts_code:
            self.ts_codes.append({
                "name": table_name,
                "content": new_ts_code
            })

    def get_ts_code_file_content(self):
        try:
            return self.render_template("table_define.ts", {
                "codes": self.ts_codes
            })
        except Exception as e:
            print("get ts code file content error!", self.ts_codes, e)
            return ""

    def _generate_ts_code(self, table_name, table_sheet):
        try:
            return self.render_template("table_implements.ts", {
                "table": {
                    "name": table_name,
                    "properties": table_sheet.get_fields()
                }
            })
        except Exception as e:
            print("export ts code error!", table_name, table_sheet, e)
            return ""

    def get_ts_code_manager_file_content(self):
        try:
            return self.render_template(self.get_table_manager_template_file_name(), {
                "tables": [key for key in self.ts_codes]
            })
        except Exception as e:
            print("get ts code manager file content error!", self.ts_codes, e)
            return ""

    def get_ts_code_table_instances_content(self):
        try:
            return self.render_template("table_instances.ts", {
                "tables": [key for key in self.ts_codes]
            })
        except Exception as e:
            print("get ts code urls content error!", self.ts_codes, e)
            return ""

    def render_template(self, template_name, config):
        print(f"render template [{template_name}] : start")
        context = self.context_generator.generate_context(config)
        render_ret = self.render(template_name, context)
        print(f"render template [{template_name}] : finish")
        return render_ret

    def get_table_manager_template_file_name(self):
        return "bundle_table_manager.ts" if self.context_generator.get_prefix() else "project_table_manager.ts"
