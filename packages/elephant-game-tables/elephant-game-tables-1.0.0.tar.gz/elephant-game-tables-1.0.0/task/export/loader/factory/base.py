class ScopeLoaderFactory:
    def __init__(self):
        self.loaders = []
        self._init_scope_loaders()

    def _init_scope_loaders(self):
        pass

    def append_loader(self, loader_cls):
        self.loaders.append(loader_cls)

    def get_loader(self, scope):
        for loader in self.loaders:
            if loader.is_scope(scope):
                return loader()
        return None
