from sheet.excel_table_sheet import ExcelTableSheet
from sheet.step.parse_phase import ParsePhase
from sheet.table_sheets import TableSheet


class TableSheetManager:
    def __init__(self):
        self.sheets = {}

    def has_sheets(self):
        return len(self.sheets.items()) > 0

    def load_all_sheets(self, files):
        for file in files:
            new_table_sheets = TableSheet.load_file(ExcelTableSheet, self, file)
            for sheet_name, sheet in new_table_sheets.items():
                if self._filter_table_sheets(sheet_name):
                    table_sheet_name = f"{sheet_name}Table"
                    self.sheets[table_sheet_name] = sheet  # 这里统一添加Table后缀
        print(f"load all table sheets finish. count=>[{len(self.sheets)}]")

    @staticmethod
    def _filter_table_sheets(sheet_name):
        return False if '@' in sheet_name else True

    def get_sheet(self, sheet_name):
        return self.sheets[sheet_name]

    def get_all_sheets(self):
        return self.sheets

    def merge_tables(self):
        for sheet in self.sheets.values():
            sheet.parse(ParsePhase.MergeTable)
