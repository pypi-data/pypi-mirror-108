from sheet.step.boundary_based import BoundaryBasedParseStep


class FoldingStep(BoundaryBasedParseStep):
    __step_name__ = "folding"

    def _on_parse_phase(self):
        return True

    # def _execute_folding(self):
    #     while (True):
    #         foldingType = None
    #         # 查找右侧括号#
    #         for i in range(len(self.fieldList)):
    #             field = self.fieldList[i]
    #             folding = field.folding
    #             if folding == None or folding == '':
    #                 continue
    #
    #             if folding[0] == '}':
    #                 foldingType = "brace"
    #             elif folding[0] == ']':
    #                 foldingType = "bracket"
    #             else:  # 未找到右括号，进入下一轮循环
    #                 continue
    #
    #             # 记录折叠终止格
    #             endIndex = i
    #
    #             # 清除括号
    #             field.folding = folding[1:]
    #             break
    #
    #         # 未找到折叠字段类型，就跳出
    #         if foldingType == None:
    #             break
    #
    #         # 查找左侧括号#
    #         for i in range(endIndex - 1, -1, -1):
    #             field = self.fieldList[i]
    #             folding = field.folding
    #             if folding == None or folding == '':
    #                 continue
    #
    #             if foldingType == "brace":
    #                 bracketIndex = folding.rfind('{')
    #             elif foldingType == "bracket":
    #                 bracketIndex = folding.rfind('[')
    #
    #             # 未找到括号，跳过
    #             if bracketIndex == -1:
    #                 continue
    #
    #             # 记录折叠起始格
    #             startIndex = i
    #
    #             # 取折叠后的名字
    #             foldingName = folding[bracketIndex + 1:]
    #
    #             # 清除括号和名字
    #             field.folding = folding[:bracketIndex]
    #             break
    #
    #         # 折叠数据#
    #         for row in range(self.dataStartRow, self.data_end_row):
    #             # 取记录
    #             recordId = self.__get_record_id(row)
    #             record = self.python_obj[recordId]
    #
    #             # 生成新对象
    #             if foldingType == "brace":
    #                 foldingObj = {}
    #             elif foldingType == "bracket":
    #                 foldingObj = []
    #
    #             for col in range(startIndex, endIndex + 1):
    #                 field = self.fieldList[col]
    #
    #                 # 保存折叠后的数据
    #                 if foldingType == "brace":
    #                     foldingObj[field.name] = record[field.name]
    #                 elif foldingType == "bracket":
    #                     foldingObj.append(record[field.name])
    #
    #                 del record[field.name]
    #
    #             # 挂接新对象
    #             record[foldingName] = foldingObj
    #
    #         # 折叠字段#
    #         # 需要清除的字段索引表
    #         delFieldList = []
    #         for col in range(startIndex + 1, endIndex + 1):
    #             field = self.fieldList[col]
    #             delFieldList.append(field)
    #
    #         # 如果最后一格有内容，则复制给合并后的格子
    #         if field.folding != None or field.folding != '':
    #             folding = field.folding
    #         else:
    #             folding = None
    #
    #         # 执行清除
    #         for field in delFieldList:
    #             self.fieldList.remove(field)
    #
    #         # 刷新折叠后的字段
    #         field = self.fieldList[startIndex]
    #         field.name = foldingName
    #         field.type = 'd'  # 折叠后变为字典类型
    #         if folding != None:
    #             field.folding = folding
    #
    #         # 刷新列表长度
    #         self.data_end_col -= endIndex - startIndex
