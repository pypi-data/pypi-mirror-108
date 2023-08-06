from task.export.loader.frameworks import FrameworksScopeLoader
from task.export.loader.game import GameScopeLoader
from task.export.loader.group import GroupScopeLoader
from task.export.scope import TaskScope


class AllScopeLoader(GroupScopeLoader):
    __scope__ = TaskScope.All

    def _init_sub_loaders(self):
        self.append_loader(GameScopeLoader())
        self.append_loader(FrameworksScopeLoader())
