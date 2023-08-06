from sheet.step.sole_phase_step import SolePhaseTableSheetParseStep


class TableSheetValidateStep(SolePhaseTableSheetParseStep):
    __step_name__ = "validate"

    def _on_parse_phase(self):
        return self.work_sheet.max_row > 1 and self.work_sheet.max_column > 1
