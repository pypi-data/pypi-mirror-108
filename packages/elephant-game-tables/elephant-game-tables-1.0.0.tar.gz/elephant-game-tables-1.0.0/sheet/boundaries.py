import enum

from sheet.attributes import Attributes


class BoundaryName(enum.Enum):
    Start = "start"
    Finish = "finish"


class BoundaryAttributes(Attributes):
    def set_start(self, start_val):
        self.set_boundary(BoundaryName.Start, start_val)

    @property
    def start(self):
        return self.get_boundary(BoundaryName.Start)

    def set_finish(self, finish_val):
        self.set_boundary(BoundaryName.Finish, finish_val)

    @property
    def finish(self):
        return self.get_boundary(BoundaryName.Finish)

    def get_boundary(self, boundary):
        return self.get_attribute(boundary.name, -1)

    def set_boundary(self, boundary, boundary_val):
        return self.set_attribute(boundary.name, boundary_val)
