"""Base class for all commands"""

from optparse import OptionGroup


class BaseCommand(object):

    # default settings to be used for this command instead of global defaults
    default_settings = {}

    exitcode = 0

    def __init__(self):
        self.settings = None
        self.configured = False

    def syntax(self):
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def short_desc(self):
        """
        A short description of the command
        """
        return ""

    def long_desc(self):
        """A long description of the command. Return short description when not
        available. It cannot contain newlines, since contents will be formatted
        by optparser which removes newlines and wraps text.
        """
        return self.short_desc()

    def help(self):
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines, since not post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        group = OptionGroup(parser, "Global Options")
        group.add_option("--pdb", action="store_true",
                         help="enable pdb on failure")
        parser.add_option_group(group)

    def process_options(self, args, opts):
        """
        TO DO
        """
        return ""

    def run(self, args, opts):
        """
        Entry point for running commands
        """
        raise NotImplementedError
