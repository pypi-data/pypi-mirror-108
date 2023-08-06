class AbstractTableSheetParseStep:
    __step_name__ = ""

    @classmethod
    def get_step_name(cls):
        return cls.__step_name__

    @property
    def sheet_manager(self):
        return self.table_sheet.sheet_manager

    def get_sheet(self, sheet_name):
        return self.sheet_manager.get_sheet(sheet_name)

    def __init__(self):
        self.table_sheet = None

    def cell_of(self, row, col):
        return self.work_sheet.cell(row, col)

    @property
    def work_sheet(self):
        return self.table_sheet.work_sheet

    def set_table_sheet(self, table_sheet):
        self.table_sheet = table_sheet

    def parse(self, parse_phase):
        return self._do_parse(parse_phase)

    # 子类实现的方法
    def _do_parse(self, parse_phase):
        print(f"unimplemented parse step! name={self.__step_name__}")
        return False


class TableSheetParser:
    def __init__(self, table_sheet):
        self.table_sheet = table_sheet
        self.steps = []

    def append_step(self, step):
        step.set_table_sheet(self.table_sheet)
        self.steps.append(step)

    def start_parse(self, parse_phase):
        for step in self.steps:
            if not step.parse(parse_phase):
                return False
        return True
