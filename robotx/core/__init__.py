"""Dealing with all general issues about command line tool set.

And this is command entry point.
"""

import sys
import inspect
import optparse

from robotx.core.base import BaseCommand
from robotx.utils.misc import walk_modules
from robotx.core.exceptions import UsageError


def _iter_command_classes(module_name):
    """generator for getting cmd"""
    for module in walk_modules(module_name):
        for obj in vars(module).itervalues():
            if inspect.isclass(obj) and \
               issubclass(obj, BaseCommand) and \
               obj.__module__ == module.__name__:
                yield obj


def _get_commands_from_module(module):
    """As subject~"""
    d = {}
    for cmd in _iter_command_classes(module):
        cmdname = cmd.__module__.split('.')[-1]
        d[cmdname] = cmd()
    return d


def _get_commands_dict(settings):
    """As subject~"""
    cmds = _get_commands_from_module('robotx.core.commands')
    return cmds


def _pop_command_name(argv):
    """As subject~"""
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1


def _print_header(settings):
    """As subject~"""
    print "RobotX - Toolset for Automation Development with Robot Framework\n"


def _print_commands(settings):
    """As subject~"""
    _print_header(settings)
    print "Usage:"
    print "    robotx <sub-command> [options] [args]\n"
    print "Available sub-commands:"
    cmds = _get_commands_dict(settings)
    for cmdname, cmdclass in sorted(cmds.iteritems()):
        print "    %-16s %s" % (cmdname, cmdclass.short_desc())
    print '\nUse "robotx <sub-command> -h" to see more info about sub-command'


def _print_unknown_command(settings, cmdname):
    """As subject~"""
    _print_header(settings)
    print "Unknown command: %s\n" % cmdname
    print 'Use "robotx" to see available commands'


def _run_print_help(parser, func, *a, **kw):
    """As subject~"""
    try:
        func(*a, **kw)
    except UsageError, e:
        if str(e):
            parser.error(str(e))
        if e.print_help:
            parser.print_help()
        sys.exit(2)


def execute(argv=None, settings=None):
    """The entry point of command line"""
    if argv is None:
        argv = sys.argv

    if settings is None:
        settings = 'nothing'

    cmds = _get_commands_dict(settings)
    cmdname = _pop_command_name(argv)
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(),
                                   conflict_handler='resolve')
    if not cmdname:
        _print_commands(settings)
        sys.exit(0)
    elif cmdname not in cmds:
        _print_unknown_command(settings, cmdname)
        sys.exit(2)

    cmd = cmds[cmdname]
    parser.usage = "robotx %s %s" % (cmdname, cmd.syntax())
    parser.description = cmd.long_desc()
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    _run_print_help(parser, cmd.process_options, args, opts)
    _run_print_help(parser, _run_command, cmd, args, opts)
    sys.exit(cmd.exitcode)


def _run_command(cmd, args, opts):
    """As subject~"""
    cmd.run(args, opts)


if __name__ == '__main__':
    execute()
