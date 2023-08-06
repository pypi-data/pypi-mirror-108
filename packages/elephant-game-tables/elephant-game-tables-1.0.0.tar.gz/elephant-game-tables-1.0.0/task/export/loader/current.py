from task.export.loader.frameworks import FrameworksScopeLoader
from task.export.loader.game import GameScopeLoader
from task.export.loader.group import GroupScopeLoader
from task.export.scope import TaskScope


class CurrentScopeLoader(GroupScopeLoader):
    __scope__ = TaskScope.Current

    def load_tasks(self):
        dynamic_loader = self._dynamic_create_loader_from_input_path()
        if dynamic_loader:
            self.append_loader(dynamic_loader)
            return super().load_tasks()
        return []

    def _dynamic_create_loader_from_input_path(self):
        if self.project_paths.is_project_path(self.input_dir):
            return GameScopeLoader()
        if self.project_paths.is_business_bundle_path(self.input_dir):
            frameworks_scope_loader = FrameworksScopeLoader()
            business_bundle_name = self.project_paths.get_business_bundle_name_of(self.input_dir)
            frameworks_scope_loader.set_white_list([business_bundle_name])
            return frameworks_scope_loader
        return None
