from task.export.loader.abstract import AbstractScopeLoader


class GroupScopeLoader(AbstractScopeLoader):
    def __init__(self):
        super(GroupScopeLoader, self).__init__()
        self.sub_loaders = []
        self._init_sub_loaders()

    def append_loader(self, sub_loader):
        self.sub_loaders.append(sub_loader)

    def _init_sub_loaders(self):
        pass

    def load_tasks(self):
        for sub_loader in self.sub_loaders:
            sub_loader.bind_task(self.task)
            yield from sub_loader.load_tasks()
