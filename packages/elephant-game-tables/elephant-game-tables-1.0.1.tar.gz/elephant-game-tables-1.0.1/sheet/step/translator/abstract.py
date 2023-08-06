class AbstractValueTranslator:
    @classmethod
    def is_value_type(cls, value_type):
        return False

    def translate_value(self, value_type, value, field):
        return value

    def get_default_value(self):
        return None
