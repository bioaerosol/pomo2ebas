""" Supplies default parameter values. """
import yaml


class Defaults(object):
    """Defaults store that supplies defaults for commands and parameters."""

    def __init__(self, config_file=r"yaml\defaults.yaml"):
        with open(config_file, "r") as cf:
            self.defaults = yaml.load(cf, Loader=yaml.FullLoader)

    def get_default(self, command: str, parameter: str):
        """Returns a default value for the given command and parameter or None if no such value exists."""
        if command in self.defaults.keys():
            if parameter in self.defaults[command]:
                return self.defaults[command][parameter]

        return None
