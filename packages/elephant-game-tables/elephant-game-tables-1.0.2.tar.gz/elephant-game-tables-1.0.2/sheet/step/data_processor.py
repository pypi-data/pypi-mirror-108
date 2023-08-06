from sheet.step.boundary_based import BoundaryBasedParseStep
from sheet.step.parse_phase import ParsePhase


class DataProcessorStep(BoundaryBasedParseStep):
    # 获得当前行的recordId
    def _get_record_id(self, row_index):
        record_cell = self.cell_of(row_index, 1)
        record_id = record_cell.value
        try:
            return int(record_id)
        except:
            return record_id

    def _extract_data_rows(self):
        for row_index in self.all_rows:
            record_id = self._get_record_id(row_index)
            if str(record_id)[0] == '#':  # 注释
                continue
            yield row_index, record_id

    @property
    def all_data_cells(self):
        fields = self.table_sheet.fields
        for row_index, record_id in self._extract_data_rows():
            for col_index in self.all_cols:
                col_field = fields[col_index - 1]
                yield row_index, col_index, record_id, col_field, self.cell_of(row_index, col_index)


class PostDataProcessorStep(DataProcessorStep):
    __parse_phase__ = ParsePhase.MergeTable

    def get_record(self, record_id):
        return self.table_sheet.contents[record_id]

    @property
    def all_records(self):
        for row_index, record_id in self._extract_data_rows():
            yield row_index, self.get_record(record_id)
