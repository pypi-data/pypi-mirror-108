import enum


class ParsePhase(enum.Enum):
    LoadTable = "load_table",
    MergeTable = "merge_table"
