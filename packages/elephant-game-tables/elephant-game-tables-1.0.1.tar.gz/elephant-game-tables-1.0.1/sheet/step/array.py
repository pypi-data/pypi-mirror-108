from sheet.step.translator.abstract import AbstractValueTranslator


class ArrayTranslator(AbstractValueTranslator):
    __layered_array_separators__ = "|;"

    @classmethod
    def is_value_type(cls, value_type):
        return value_type.startswith("a")

    def __init__(self, factory):
        super(ArrayTranslator, self).__init__()
        self.factory = factory

    def translate_value(self, value_type, values, field):
        array_separator = self._get_array_separator(value_type)
        if array_separator is None:
            return None
        item_value_type = value_type[1:]
        translated_values = []
        for array_item_value in values.split(array_separator):
            if array_item_value:
                translated_values.append(self._translate_single_value(item_value_type, array_item_value, field))
        return translated_values

    def _translate_single_value(self, value_type, value, field):
        return self.factory.translate_value(value_type, value, field)

    @classmethod
    def _get_array_level(cls, value_type):
        level = 0
        for c in value_type:
            if c == 'a':
                level += 1
            else:
                break
        return level

    def _get_array_separator(self, value_type):
        level = self._get_array_level(value_type)
        if level <= 0:
            print(f"无效数组类型! type=>[{value_type}]")
            return None
        max_level = len(self.__layered_array_separators__)
        if level > max_level:
            print(f"不支持数组层数嵌套层数[{level}], 当前支持最大层数=[{max_level}]")
            return None
        return self.__layered_array_separators__[level - 1]
