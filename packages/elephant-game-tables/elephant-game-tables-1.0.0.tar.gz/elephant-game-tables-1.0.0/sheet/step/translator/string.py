from sheet.step.translator.sole import SoleTypeValueTranslator


class StringTranslator(SoleTypeValueTranslator):
    __value_type__ = "s"

    def _do_translate_value(self, value):
        try:
            return str(int(value))
        except:
            return str(value)

    def get_default_value(self):
        return ""
