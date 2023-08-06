from sheet.step.translator.abstract import AbstractValueTranslator


class SoleTypeValueTranslator(AbstractValueTranslator):
    __value_type__ = ""

    @classmethod
    def get_value_type(cls):
        return cls.__value_type__

    @classmethod
    def is_value_type(cls, value_type):
        return cls.get_value_type() == value_type

    def translate_value(self, value_type, value, field):
        return self._do_translate_value(value)

    def _do_translate_value(self, value):
        return value
