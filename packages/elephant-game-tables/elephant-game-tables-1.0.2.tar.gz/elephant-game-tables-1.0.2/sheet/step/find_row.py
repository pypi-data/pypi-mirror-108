from sheet.step.row_attr import RowAttributes, RowName
from sheet.step.sole_phase_step import SolePhaseTableSheetParseStep


class FindTableRowStep(SolePhaseTableSheetParseStep):
    """查找数据起始行数，格式行，缺省值行，类型行，数据终止行数"""

    __step_name__ = "find_row"

    def _on_parse_phase(self):
        rows = RowAttributes()

        if not self._parse_named_rows(rows):
            print("parse named rows fail!")
            return False

        if not self._parse_data_boundary_rows(rows):
            print(f'parse boundary rows fail!')
            return False

        # 这里设置表格的行数据
        self.table_sheet.rows = rows
        return True

    def _parse_named_rows(self, rows):
        for name_index in range(1, len(RowName) + 1):
            cell_value = self.work_sheet.cell(name_index, 1).value
            row_name = self._try_get_row_name(cell_value)
            if row_name is not None:
                rows.set_attribute(row_name, name_index)
        return True

    def _parse_data_boundary_rows(self, rows):
        rows.set_start(self._get_start_row())
        rows.set_finish(self._get_finish_row(rows.start))
        return True

    def _get_start_row(self):
        for row_index in range(1, self.work_sheet.max_row + 1):
            cell_value = self.work_sheet.cell(row_index, 1).value
            if cell_value:
                if self._try_get_row_name(cell_value) is None:
                    return row_index
            else:
                return -1

    def _get_finish_row(self, start_row):
        if start_row == -1:
            return -1
        for row_index in range(start_row + 1, self.work_sheet.max_row + 1):
            cell_value = self.work_sheet.cell(row_index, 1).value
            if not cell_value:
                return row_index
        return self.work_sheet.max_row + 1

    @classmethod
    def _try_get_row_name(cls, row_name_tag):
        for row_name in list(RowName):
            if row_name.value == row_name_tag:
                return row_name.name
        return None
