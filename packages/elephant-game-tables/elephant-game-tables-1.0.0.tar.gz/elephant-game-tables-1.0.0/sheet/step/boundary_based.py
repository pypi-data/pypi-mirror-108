from sheet.step.sole_phase_step import SolePhaseTableSheetParseStep


class BoundaryBasedParseStep(SolePhaseTableSheetParseStep):
    @property
    def rows(self):
        return self.table_sheet.rows

    @property
    def default_row(self):
        return self.rows.default

    def default_cell(self, col):
        return self.cell_of(self.default_row, col)

    @property
    def type_row(self):
        return self.rows.type

    def type_cell(self, col):
        return self.cell_of(self.type_row, col)

    @property
    def name_row(self):
        return self.rows.name

    def name_cell(self, col):
        return self.cell_of(self.name_row, col)

    @property
    def cols(self):
        return self.table_sheet.cols

    @property
    def col_start(self):
        return self.cols.start

    @property
    def col_finish(self):
        return self.cols.finish

    @property
    def all_rows(self):
        if self.rows.start == -1 or self.rows.finish == -1:
            return
        for row_index in range(self.rows.start, self.rows.finish):
            yield row_index

    @property
    def all_cols(self):
        if self.cols.start == -1 or self.cols.finish == -1:
            return
        for col_index in range(self.cols.start, self.cols.finish):
            yield col_index

    @property
    def all_data_cols(self):
        for col_index in range(self.cols.start + 1, self.cols.finish):
            yield col_index
