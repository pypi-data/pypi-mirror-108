from sheet.step.translator.sole import SoleTypeValueTranslator


class BoolTranslator(SoleTypeValueTranslator):
    __value_type__ = "b"

    def _do_translate_value(self, value):
        return bool(value)

    def get_default_value(self):
        return False
