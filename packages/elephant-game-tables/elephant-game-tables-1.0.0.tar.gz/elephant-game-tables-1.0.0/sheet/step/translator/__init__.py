import math

from sheet.step.array import ArrayTranslator
from sheet.step.translator.bool import BoolTranslator
from sheet.step.translator.comment import CommentTranslator
from sheet.step.translator.dict import DictTranslator
from sheet.step.translator.enum import EnumTranslator
from sheet.step.translator.factory import ValueTranslatorFactory
from sheet.step.translator.float import FloatTranslator
from sheet.step.translator.int import IntTranslator
from sheet.step.translator.reference import ReferenceTranslator
from sheet.step.translator.string import StringTranslator


class AllValueTranslatorFactory(ValueTranslatorFactory):
    def _init_translators(self):
        self.append_translator(IntTranslator())
        self.append_translator(FloatTranslator())
        self.append_translator(StringTranslator())
        self.append_translator(BoolTranslator())
        self.append_translator(ArrayTranslator(self))  # 数组,支持多层嵌套
        self.append_translator(DictTranslator())  # 字典
        self.append_translator(ReferenceTranslator())  # 引用
        self.append_translator(EnumTranslator())  # 枚举
        self.append_translator(CommentTranslator())  # 注释

    def _unknown_value_type(self, value_type, value, field):
        auto_detected_value_type = self._auto_detect_value_type(value)
        success, translated_value = self._do_translate_value(auto_detected_value_type, value, field)
        return translated_value

    @classmethod
    def _auto_detect_value_type(cls, value):
        if isinstance(value, float):
            if math.ceil(value) == value:
                return 'i'
            else:
                return 'f'
        else:
            return 's'


value_translator = AllValueTranslatorFactory()
