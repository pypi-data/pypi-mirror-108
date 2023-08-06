from task.base import BaseTask
from task.export.loader.factory import scope_loader_factory
from task.export.scope import TaskScope
from task.options import ProjectTaskOptions


class ExportTableTaskOptions(ProjectTaskOptions):
    def __init__(self):
        super(ExportTableTaskOptions, self).__init__()
        self.dimensions = None
        self.scope = TaskScope.Current.value


class TableExportTask(BaseTask):
    __task_name__ = "table_export_task"

    def __init__(self, options):
        super().__init__(options)
        self.append_task_step("run_all_bundle_tasks", self._run_all_bundle_tasks)

    @property
    def dimensions(self):
        return self.options.dimensions

    @property
    def scope(self):
        return TaskScope.get_scope(self.options.scope)

    def _load_bundle_tasks(self):
        scope_loader = scope_loader_factory.get_loader(self.scope)
        scope_loader.bind_task(self)
        return scope_loader.load_tasks()

    def _run_all_bundle_tasks(self):
        for bundle_task in self._load_bundle_tasks():
            bundle_task.run()
        return True
