from sheet.step.translator.sole import SoleTypeValueTranslator


class FloatTranslator(SoleTypeValueTranslator):
    __value_type__ = "f"

    def get_default_value(self):
        return 0.0
