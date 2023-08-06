from typing import Tuple

from sheet.step.data_processor import DataProcessorStep
from sheet.step.translator import value_translator


class ParseDataStep(DataProcessorStep):
    __step_name__ = "parse_data"

    """解析自身数据为python，并折叠。不包括引用数据"""

    def _on_parse_phase(self):
        data_contents = {}
        for row_index, record_id in self._extract_data_rows():
            record = self._generate_record_of_row(row_index)
            data_contents[record_id] = record
        self.table_sheet.contents = data_contents
        return True

    def _generate_record_of_row(self, row_index):
        new_record = {}
        fields = self.table_sheet.fields
        for col_index in self.all_data_cols:
            col_field = fields[col_index - 1]
            if col_field.type == '#':  # 注释
                continue
            record_field_cell = self.cell_of(row_index, col_index)
            field_value_ret = self._get_field_value(record_field_cell, col_field)
            field_name, field_value = self._normalize_field_parts(field_value_ret, col_field)
            new_record[field_name] = field_value
        return new_record

    @classmethod
    def _normalize_field_parts(cls, field_value_ret, field):
        if isinstance(field_value_ret, Tuple):
            return field_value_ret
        return field.name, field_value_ret

    @classmethod
    def _get_field_value(cls, record_field_cell, col_field):
        cell_value = record_field_cell.value
        if not cell_value:
            return col_field.default
        if cell_value == 'null':
            return None
        return value_translator.translate_value(col_field.type, cell_value, col_field)
