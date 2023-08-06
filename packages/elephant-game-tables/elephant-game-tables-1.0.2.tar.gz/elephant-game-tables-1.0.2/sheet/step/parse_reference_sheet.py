from sheet.step.data_processor import DataProcessorStep


class ParseReferenceSheetStep(DataProcessorStep):
    def _on_parse_phase(self):
        referencing_sheets = []
        for row, col, record_id, field, cell in self.all_data_cells:
            if field.type != 'r':
                continue
            reference_sheet_name = cell.value.spit('.')[0]
            if reference_sheet_name not in referencing_sheets:
                referencing_sheets.append(reference_sheet_name)
        self.table_sheet.referencing_sheets = referencing_sheets
        return True
