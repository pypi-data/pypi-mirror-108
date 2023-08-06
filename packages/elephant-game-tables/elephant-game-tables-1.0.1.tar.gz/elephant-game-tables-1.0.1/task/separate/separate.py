import os

from dimension.table_dimension_spreader import TableSpreader
from task.base import BaseTask
from task.options import ProjectTaskOptions


class SeparateTaskOptions(ProjectTaskOptions):
    def __init__(self):
        super(SeparateTaskOptions, self).__init__()


class SeparateTask(BaseTask):
    __task_name__ = "separate_excel_files_task"

    def __init__(self, options):
        super().__init__(options)
        self.append_task_step("spread_tables", self._spread_tables)

    def _spread_tables(self):
        table_dir = self.project_path_manager.get_table_dir()
        if not os.path.exists(table_dir):
            print(f"table dir NOT exist! table_die=>[{table_dir}]")
            return False

        table_spreader = TableSpreader()
        table_spreader.spread_all(table_dir)
        return True
