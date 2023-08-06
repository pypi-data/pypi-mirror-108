from sheet.boundaries import BoundaryAttributes


class ColAttributes(BoundaryAttributes):
    def __init__(self):
        super().__init__()
        self.set_start(1)  # openpyxl是从下标1开始的
