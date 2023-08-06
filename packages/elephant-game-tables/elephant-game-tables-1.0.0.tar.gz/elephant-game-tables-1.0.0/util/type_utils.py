class TypeUtils:
    @staticmethod
    def get_typescript_type_of(field_type):
        if field_type == 'i':
            return "number"
        elif field_type == 'f':
            return "number"
        elif field_type == 's':
            return "string"
        elif field_type == 'b':
            return "boolean"
        elif field_type == 'as':
            return "string[]"
        elif field_type == 'ass':
            return "string[][]"
        elif field_type == 'aff' or field_type == 'aii':
            return "number[][]"
        elif field_type == 'ai' or field_type == 'af':
            return "number[]"
        elif field_type == 'd':
            return "{[index:string]: any}"
        elif field_type == 'r':  # 引用，保存引用字符串，以备插入引用表
            return "any"
        elif field_type.find('$') == 0:
            return field_type[1:]
        elif field_type.find('%') == 0:
            return field_type[1:]
