import enum

from sheet.boundaries import BoundaryAttributes


class RowName(enum.Enum):
    Default = '__default__'
    Folding = '__folding__'
    Type = '__type__'
    Name = '__name__'
    Desc = '__desc__'


class RowAttributes(BoundaryAttributes):
    def get_row(self, row):
        return self.get_row_by_name(row.name)

    def get_row_by_name(self, row_name):
        return self.get_attribute(row_name, -1)

    @property
    def default(self):
        return self.get_row(RowName.Default)

    @property
    def folding(self):
        return self.get_row(RowName.Folding)

    @property
    def type(self):
        return self.get_row(RowName.Type)

    @property
    def name(self):
        return self.get_row(RowName.Name)

    @property
    def desc(self):
        return self.get_row(RowName.Desc)
