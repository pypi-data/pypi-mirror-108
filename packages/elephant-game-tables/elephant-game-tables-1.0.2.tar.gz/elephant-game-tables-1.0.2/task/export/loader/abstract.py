class AbstractScopeLoader:
    __scope__ = None

    @classmethod
    def scope(cls):
        return cls.__scope__

    @classmethod
    def is_scope(cls, scope):
        return cls.scope() == scope

    def __init__(self):
        self.task = None

    @property
    def project_paths(self):
        return self.task.project_paths

    @property
    def input_dir(self):
        return self.task.input_dir

    @property
    def project_dir(self):
        return self.project_paths.project_dir

    @property
    def dimensions(self):
        return self.task.dimensions

    def bind_task(self, task):
        self.task = task

    def load_tasks(self):
        return []
