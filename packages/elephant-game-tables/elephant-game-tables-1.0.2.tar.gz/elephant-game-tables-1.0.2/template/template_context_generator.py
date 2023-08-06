from datetime import datetime


def get_date_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class TemplateContextGenerator:
    def __init__(self, prefix):
        self.prefix = prefix

    def generate_context(self, context_in):
        context_out = context_in if context_in else {}
        context_out['date'] = get_date_now()
        context_out['prefix'] = self.prefix
        return context_out

    def get_prefix(self):
        return self.prefix
