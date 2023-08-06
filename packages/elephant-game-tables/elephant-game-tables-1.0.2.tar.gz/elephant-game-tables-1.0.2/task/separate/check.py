import os

from dimension.table_dimension_check import TableDimensionCheck
from task.base import BaseTask
from task.options import ProjectTaskOptions


class CheckSeparateTaskOptions(ProjectTaskOptions):
    def __init__(self):
        super(CheckSeparateTaskOptions, self).__init__()
        self.check_files = None


class CheckSeparateTask(BaseTask):
    __task_name__ = "check_separate_excel_files_task"

    def __init__(self, options):
        super().__init__(options)
        self.append_task_step("check_table_spread_result", self._check_table_spread_result)

    def _check_table_spread_result(self):
        check_input = self.options.get_option("check")
        if not os.path.exists(check_input):
            print(f"check input dir NOT exist! check_input=>[{check_input}]")
            return False

        table_dimension_check = TableDimensionCheck(self.input_dir)
        table_dimension_check.check_all(check_input)
        return True
