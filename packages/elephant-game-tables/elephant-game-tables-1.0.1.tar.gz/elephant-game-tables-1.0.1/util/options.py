from getopt import getopt


class CommandOptions:
    @staticmethod
    def create_command_options(configs):
        config_list = []
        for config in configs.split(';'):
            config_parts = config.split(":")
            new_config = {
                "key": config_parts[0] if len(config_parts) > 0 else "",
                "sn": config_parts[1] if len(config_parts) > 1 else "",
                "fn": config_parts[2] if len(config_parts) > 2 else "",
                "dv": config_parts[3] if len(config_parts) > 3 else "",
            }
            if new_config['fn'] == '':
                new_config['fn'] = new_config['key']
            config_list.append(new_config)
        return CommandOptions(config_list)

    def __init__(self, config):
        self.configs = config
        self.options = {}

    def parse_args(self, argv):
        options, _ = getopt(argv, self._get_short_name_options(), self._get_full_name_options())
        for opt, arg in options:
            self._set_option(opt, arg)

    def _set_option(self, opt, arg):
        opt_name = opt.lstrip('-')
        for config in self.configs:
            if opt_name in (config['sn'], config['fn']):
                self.set_option(config['key'], arg)
                break

    def set_option(self, key, value):
        self.options[key] = value

    def _get_short_name_options(self):
        short_names = ""
        for config in self.configs:
            short_names += f"{config['sn']}:"
        return short_names

    def _get_full_name_options(self):
        full_names = []
        for config in self.configs:
            full_names.append(f"--{config['fn']}")
        return full_names

    def get_option(self, key, default_value=None):
        if key in self.options:
            return self.options[key]
        for config in self.configs:
            if key == config['key']:
                return config['dv']
        return default_value
