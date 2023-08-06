from sheet.step.boundary_based import BoundaryBasedParseStep
from sheet.step.translator import value_translator
from sheet.table_field import TableField


class ParseFieldStep(BoundaryBasedParseStep):
    """解析字段属性"""

    __step_name__ = "parse_properties"

    def _on_parse_phase(self):
        fields = []
        for col in range(1, self.col_finish):
            field = self._generate_new_field(col)
            fields.append(field)
        self.table_sheet.fields = fields
        return True

    def _generate_new_field(self, col):
        field = TableField()
        field.type = self.type_cell(col).value
        field.name = self.name_cell(col).value
        field.default = self._get_field_default_val(col, field.type)
        return field

    def _get_field_default_val(self, col, field_type):
        if self.default_row == -1:
            return None
        if col == 1:
            # 第一位缺省值，占位符
            return None
        default_col_cell = self.default_cell(col)
        if not default_col_cell.value:
            # 空白格
            return None
        if default_col_cell.value == 'null':
            # null格
            return None

        return value_translator.get_default_value(field_type)
