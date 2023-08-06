class Attributes:
    def __init__(self):
        self.attributes = {}

    def set_attribute(self, name, boundary):
        self.attributes[name] = boundary

    def get_attribute(self, name, default_val=None):
        return self.attributes[name] if name in self.attributes else default_val
