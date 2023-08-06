from sheet.step.data_processor import PostDataProcessorStep


class MergeReferenceSheetStep(PostDataProcessorStep):
    @property
    def all_reference_field(self):
        for col_index, field in enumerate(self.table_sheet.fields, 1):
            if field.type == 'r':
                yield col_index, field

    def _on_parse_phase(self):
        if self.table_sheet.referencing_sheets is None or len(self.table_sheet.referencing_sheets) == 0:
            return True
        return self._do_merge_references()

    def _do_merge_references(self):
        for _, record in self.all_records:
            self._merge_reference_on_record(record)
        return True

    def _merge_reference_on_record(self, record):
        for col_index, field in self.all_reference_field:
            reference_sheet_name, reference_record_id = self._parse_sheet_name_id(record[field.name])
            reference_sheet = self.get_sheet(reference_sheet_name)
            reference_sheet_contents = reference_sheet.get_contents()
            record[field.name] = reference_sheet_contents[reference_record_id]

    @classmethod
    def _parse_sheet_name_id(cls, reference_target):
        sheet_name, record_id = reference_target.split('.')
        if record_id.isdigit():
            record_id = int(record_id)
        return sheet_name, record_id
