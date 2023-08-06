from sheet.step.translator.sole import SoleTypeValueTranslator


class DictTranslator(SoleTypeValueTranslator):
    __value_type__ = "d"

    def _do_translate_value(self, value):
        translated_value = {}
        for v in value.split(";"):
            key, value = v.split("=")
            translated_value[key] = self._translate_val(value)

    @classmethod
    def _translate_val(cls, value):
        if value.isdigit() and '.' in value:
            return float(value)
        if value.isdigit():
            return int(value)
        return value
