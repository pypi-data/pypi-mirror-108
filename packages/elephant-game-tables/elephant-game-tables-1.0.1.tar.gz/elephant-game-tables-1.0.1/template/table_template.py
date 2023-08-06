import os
import sys

from jinja2 import Environment, FileSystemLoader


class RelativeFileSystemLoader(FileSystemLoader):
    def __init__(self, template_dir):
        super().__init__(template_dir)
        self.template_dir = template_dir

    def get_source(self, environment, template):
        relative_template_path = os.path.relpath(os.path.normpath(os.path.join(self.template_dir, template)), self.template_dir)
        relative_template = relative_template_path.replace("\\", '/')
        return super().get_source(environment, relative_template)


class TableTemplate:
    def __init__(self):
        templates_dir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), "./config/templates"))
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True
        )

    def render(self, file_name, content_args):
        try:
            template = self.env.get_template(f"{file_name}.j2")
            return template.render(content_args)
        except Exception as e:
            print(f"render content to file error! error=>[{e}]")
