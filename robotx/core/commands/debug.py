"""Sub command: debug

Usage: robotx debug
"""

import os
import sys
import tempfile

from robotx.core.base import BaseCommand


class Command(BaseCommand):
    """Sub command 'debug' class."""

    def syntax(self):
        """Sub command 'debug' running format"""
        return ""

    def short_desc(self):
        """Sub command 'debug' short description"""
        return "Debug Robot case, Keyword, Library"

    def long_desc(self):
        """Sub command 'debug' long description"""
        return "Enter into Robotframework debug module, \n \
                and ... \n \
                ..."

    def run(self, args, opts):
        """Sub command 'debug' runner"""
        source = tempfile.NamedTemporaryFile(prefix='robot_debug',
                                             suffix='.txt', delete=False)
        source.write('''*** Settings ***
Library    robotx.lib.DebugLibrary.Debug

** Test Cases **
A Debug Case
    debug
''')
        source.flush()
        args = '-L TRACE ' + source.name
        try:
            from robot import run_cli
            rc = run_cli(args.split())
        except ImportError:
            import robot.runner
            rc = robot.run_from_cli(args.split(), robot.runner.__doc__)
        source.close()
        if os.path.exists(source.name):
            os.unlink(source.name)
        sys.exit(rc)
