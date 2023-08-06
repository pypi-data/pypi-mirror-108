from sheet.step.col_attr import ColAttributes
from sheet.step.sole_phase_step import SolePhaseTableSheetParseStep


class FindTableColStep(SolePhaseTableSheetParseStep):
    """查找数据终止列数"""

    __step_name__ = "find_col"

    @property
    def rows(self):
        return self.table_sheet.rows

    @property
    def name_row(self):
        return self.rows.name

    def _on_parse_phase(self):
        cols = ColAttributes()
        cols.set_finish(self._get_finish_col())
        self.table_sheet.cols = cols
        return True

    def _get_finish_col(self):
        # 遍历查找，如果在excel中存在多余的注释，列数为第一个空字符串出现的单元格下标#
        name_row = self.name_row
        if name_row != -1:
            for col_index in range(1, self.work_sheet.max_column + 1):
                if not self.work_sheet.cell(name_row, col_index).value:
                    return col_index
        return self.work_sheet.max_column + 1
