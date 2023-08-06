from sheet.step.translator.multi import MultiTypeValueTranslator


class EnumTranslator(MultiTypeValueTranslator):
    __value_types__ = ["$", "%"]

    @classmethod
    def _is_target_value_type(cls, support_value_type, value_type):
        return value_type.startswith(support_value_type)

    __enum_prefixes__ = ["EM", "PEM"]

    def translate_value(self, value_type, value, field):
        enum_prefix = self._get_enum_prefix_by_type(value_type)
        return self._generate_field_name(enum_prefix, field), value

    @classmethod
    def _generate_field_name(cls, prefix, field):
        return f"{prefix}_{field.type[1:]}__{field.name}"

    def _get_enum_prefix_by_type(self, value_type):
        type_index = self.__value_types__.index(value_type)
        return self.__enum_prefixes__[type_index]
