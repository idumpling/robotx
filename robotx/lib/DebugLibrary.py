"""
RobotFramework Debug Library.

* Import this library, and type keyword "debug", then run case with pybot,
* such as:  Library    robotx.lib.DebugLibrary.Debug
  then make your program stop on specified line.
* Directly enter into debug shell, and try to do sth.

Author: Xin Gao <fdumpling@gmail.com>
"""

import re
import sys
from cmd import Cmd

from robot.libraries.BuiltIn import BuiltIn
from robot.errors import HandlerExecutionFailed


class Debug:
    """RobotFramework debug library
    """

    def debug(self):
        '''Type this keyword to anywhere you want to stop and debug
        on your Robot Framework case.
        '''
        old_stdout = sys.stdout
        sys.stdout = sys.__stdout__
        print '\n\nEnter into Robot Framework debug shell:'
        debug_cmd = DebugCmd()
        debug_cmd.cmdloop()
        print '\nExit Robot Framework debug shell.'
        sys.stdout = old_stdout


class DebugCmd(Cmd):
    """Interactive debug shell
    """

    use_rawinput = True
    prompt = '>>> '

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        Cmd.__init__(self, completekey, stdin, stdout)
        self.rf_bi = BuiltIn()

    def default(self, line):
        """Run RobotFramework keywords
        """
        pattern = re.compile('  +|\t')
        command = line.strip()
        if not command:
            return
        try:
            keyword = pattern.split(command)
            result = self.rf_bi.run_keyword(*keyword)
            if result:
                print repr(result)
        except HandlerExecutionFailed, exc:
            print 'keyword: ', command
            print '! ', exc.full_message
        except Exception, exc:
            print 'keyword: ', command
            print '! FAILED: ', repr(exc)

    def emptyline(self):
        """By default Cmd runs last command if an empty line is entered.
        Disable it.
        """
        pass

    def postcmd(self, stop, line):
        """run after a command"""
        return stop

    def do_exit(self, arg):
        """Exit
        """
        return True

    def do_web(self, arg):
        """Do web automation debug"""
        print 'import library  Selenium2Library'
        self.rf_bi.run_keyword('import library', 'Selenium2Library')
        if arg:
            url = arg
        else:
            url = 'http://www.google.com/'
        print 'open browser  %s' % url
        self.rf_bi.run_keyword('Open Browser', url)

    def help_help(self):
        """Help of Help command
        """
        print 'Show help message.'

    def help_exit(self):
        """Help of Exit command
        """
        print 'Exit the interpreter.'
        print 'Use exit() or Ctrl-D (i.e. EOF) to exit'

    def help_web(self):
        '''Help of web command'''
        print 'Do some web automation with Selenium2Library'

    do_EOF = do_exit
    help_EOF = help_exit
