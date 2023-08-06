from sheet.step.translator.sole import SoleTypeValueTranslator


class IntTranslator(SoleTypeValueTranslator):
    __value_type__ = "i"

    def _do_translate_value(self, value):
        return int(value)

    def get_default_value(self):
        return 0
