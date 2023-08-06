from sheet.step.parse_phase import ParsePhase
from sheet.step.parse_step import AbstractTableSheetParseStep


class SolePhaseTableSheetParseStep(AbstractTableSheetParseStep):
    __parse_phase__ = ParsePhase.LoadTable

    def _do_parse(self, parse_phase):
        if parse_phase != self.__parse_phase__:
            return True
        return self._on_parse_phase()

    def _on_parse_phase(self):
        print(f"unimplemented phase parse step! name={self.__step_name__}, phase={self.__parse_phase__}")
        return False
