class TableField:
    def __init__(self):
        # 字段名
        self.name = None
        # 字段类型
        self.type = None
        # 缺省值
        self.default = None
        # 折叠属性
        self.folding = None

    def __str__(self):
        return "name:%r,type:%r,default:%r,folding:%r" % (self.name, self.type, self.default, self.folding)
