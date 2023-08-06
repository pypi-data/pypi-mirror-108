import os

from task.abstract import AbstractTask
from util.project_path import ProjectPathManager


class BaseTask(AbstractTask):
    def __init__(self, options):
        super().__init__()
        self.append_task_step("parse_command", self._parse_command)
        self.options = options
        self.project_paths = ProjectPathManager(options.input_dir)

    @property
    def input_dir(self):
        return os.path.abspath(self.options.input_dir)

    def _parse_command(self):
        if not os.path.exists(self.input_dir):
            print(f"project dir NOT exist! project_dir=>[{self.input_dir}]")
            return False
        return True
