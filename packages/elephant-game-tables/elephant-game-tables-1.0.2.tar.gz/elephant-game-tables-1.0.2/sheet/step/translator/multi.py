from sheet.step.translator.abstract import AbstractValueTranslator


class MultiTypeValueTranslator(AbstractValueTranslator):
    __value_types__ = []

    @classmethod
    def is_value_type(cls, value_type):
        for support_value_type in cls.__value_types__:
            cls._is_target_value_type(support_value_type, value_type)

    @classmethod
    def _is_target_value_type(cls, support_value_type, value_type):
        return support_value_type == value_type
