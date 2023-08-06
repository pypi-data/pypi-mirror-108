import enum


class TaskScope(enum.Enum):
    Current = "current"
    All = "all"
    Frameworks = "frameworks"
    Game = "game"

    @classmethod
    def get_scope(cls, scope_name):
        for scope in TaskScope:
            if scope.value == scope_name:
                return scope
        return TaskScope.Current
