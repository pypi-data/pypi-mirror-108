class ValueTranslatorFactory:
    def __init__(self):
        self.translators = []
        self._init_translators()

    def _init_translators(self):
        pass

    def append_translator(self, new_translator):
        self.translators.append(new_translator)

    def translate_value(self, value_type, value, field):
        success, translated_value = self._do_translate_value(value_type, value, field)
        if success:
            return translated_value
        return self._unknown_value_type(value_type, value, field)

    def _do_translate_value(self, value_type, value, field):
        for translator in self.translators:
            if translator.is_value_type(value_type):
                return True, translator.translate_value(value_type, value, field)
        return False, None

    def _unknown_value_type(self, value_type, value, field):
        return None
