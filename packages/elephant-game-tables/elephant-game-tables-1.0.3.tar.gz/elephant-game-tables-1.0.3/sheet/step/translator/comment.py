from sheet.step.translator.sole import SoleTypeValueTranslator


class CommentTranslator(SoleTypeValueTranslator):
    __value_type__ = "#"

    def _do_translate_value(self, value):
        return None

    def get_default_value(self):
        return None
