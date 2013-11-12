"""Sub command: check

Usage: robotx check [options]
"""

import os
import tempfile

from robot import run
from robot.api import ExecutionResult

from robotx.core.base import BaseCommand
from robotx.core.nitrateclient import TCMS
from robotx.core.exceptions import UsageError
from robotx.core.resultvistor import ResultChecker
from robotx.core.resultvistor import DryRunChecker


class Command(BaseCommand):
    """Sub command 'check' class."""

    def syntax(self):
        """Sub command 'check' running format"""
        return "[-option]"

    def short_desc(self):
        """Sub command 'check' short description"""
        return "Check and validate Robot case and tag syntex"

    def long_desc(self):
        """Sub command 'check' long description"""
        return "Run without executing keywords originating\
               \nfrom test libraries.\
               \nIt's useful for validating test data syntax."

    def add_options(self, parser):
        """Sub command 'check' options"""
        parser.add_option('--tcms', action='store_true', dest='is_tcms',
                          help='Whether check cases for running with TCMS. \
                          default is no tcms checking.')
        parser.add_option("-c", "--cases", dest="cases",
                          metavar="CASES_PATH", help="Set Cases_PATH")
        parser.add_option("-p", "--planid", dest="plan_id",
                          metavar="PLAN_ID", help="Set PLAN_ID")

    def run(self, args, opts):
        """Sub command 'check' runner"""
        if not opts.cases:
            raise UsageError("case path must be set with -c or --cases!")
        print " Syntax Checking ".center(70, '*')
        print '...'
        log_level = 'TRACE'
        cases_path = opts.cases
        tmp_path = tempfile.gettempdir()
        xml_result = os.path.join(tmp_path, "check_result.xml")
        output_file = os.path.join(tmp_path, "stdout.txt")
        with open(output_file, 'w') as stdout:
            dryrun_result = run(cases_path,
                                dryrun=True,
                                loglevel=log_level,
                                log='NONE',
                                report='NONE',
                                output=xml_result,
                                stdout=stdout)
        detail_result = ExecutionResult(xml_result)
        if opts.is_tcms:
            if not opts.plan_id:
                raise UsageError("plan id must be set with -p or --planid!")
            plan_id = opts.plan_id
            tcms = TCMS()
            ids = tcms.get_plan_case_ids(plan_id)
            detail_result.visit(ResultChecker(ids, plan_id))
        elif dryrun_result == 0:
            print 'Contratulations, no syntax error'
        else:
            detail_result.visit(DryRunChecker())
        print '\n( No news is good news:) )'
        print 'checing result is in the file: %s' % output_file
        print ' DONE '.center(70, '*')
