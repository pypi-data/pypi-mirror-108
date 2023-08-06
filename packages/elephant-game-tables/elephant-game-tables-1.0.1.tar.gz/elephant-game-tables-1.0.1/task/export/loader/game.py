import os

from task.export.bundle import BundleTableExportTask
from task.export.loader.abstract import AbstractScopeLoader
from task.export.scope import TaskScope
from transform.resource_manager import GameResourceManager


class GameScopeLoader(AbstractScopeLoader):
    __scope__ = TaskScope.Game

    def load_tasks(self):
        if not os.path.exists(self.project_dir):
            print(f"project dir NOT exist! project_dir=>[{self.project_dir}]")
            return
        # 当前项目的主表目录
        game_resource_manager = GameResourceManager(self.project_dir)
        if game_resource_manager.is_table_dir_exist():
            yield BundleTableExportTask(self, game_resource_manager, '')
