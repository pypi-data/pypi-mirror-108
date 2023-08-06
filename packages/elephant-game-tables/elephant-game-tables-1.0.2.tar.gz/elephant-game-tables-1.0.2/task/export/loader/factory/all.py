from task.export.loader.all import AllScopeLoader
from task.export.loader.current import CurrentScopeLoader
from task.export.loader.factory.base import ScopeLoaderFactory
from task.export.loader.frameworks import FrameworksScopeLoader
from task.export.loader.game import GameScopeLoader


class AllScopeLoaderFactory(ScopeLoaderFactory):
    def _init_scope_loaders(self):
        self.append_loader(AllScopeLoader)
        self.append_loader(GameScopeLoader)
        self.append_loader(FrameworksScopeLoader)
        self.append_loader(CurrentScopeLoader)
