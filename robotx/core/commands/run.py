"""Sub command: run

Usage: robotx run [options]
"""

import sys

from robot import run

from robotx.core.base import BaseCommand
from robotx.core.nitrateclient import TCMS
from robotx.core.exceptions import UsageError
from robotx.core.paramshandler import ParamsHandler


class Command(BaseCommand):
    """Sub command 'run' class."""

    def syntax(self):
        """Sub command 'run' running format"""
        return "[-option]"

    def short_desc(self):
        return "Run project with or without jenjins, TCMS"

    def long_desc(self):
        """Sub command 'run' long description"""
        return "Run project with jenkins. \n \
                If y don't want to wrirte result to tcms, add --notcms. \n \
                Default is writting."

    def add_options(self, parser):
        """Sub command 'run' options"""
        parser.add_option('--jenkins', action='store_true', dest='is_jenkins',
                          help='Whether run project in jenkins. \
                          default is running in local.')
        parser.add_option('--tcms', action='store_true', dest='is_tcms',
                          help='Whether write result to tcms in real-time. \
                          default is running without tcms.')
        parser.add_option("-c", "--cases", dest="cases",
                          metavar="CASES_PATH", help="Set Cases_PATH")
        parser.add_option("-p", "--planid", dest="plan_id",
                          metavar="PLAN_ID", help="Set PLAN_ID")
        parser.add_option("-r", "--runid", dest="run_id", default='',
                          metavar="RUN_ID", help="Set RUN_ID")
        parser.add_option("-o", "--output", dest="output_dir", default='./',
                          metavar="OUTPUT_DIR", help="Set OUTput_DIR")
        parser.add_option("-t", "--tags", dest="case_tags", action="append",
                          default=[], metavar="CASE_TAGS",
                          help="Select case via CASE_TAG")
        parser.add_option("--priorities", dest="case_priorities",
                          action="append", default=[],
                          metavar="CASE_PRIORITIES",
                          help="Select case via CASE_PRIORITIES")
        parser.add_option("--variable", dest="other_variables",
                          action="append", default=[],
                          metavar="OTHER_VARIABLES",
                          help="Dynamically set variables via OTHER_VARIABLES")

    def run(self, args, opts):
        """Sub command 'run' runner"""
        tcms = TCMS()
        log_level = 'DEBUG'
        noncritical = ['noncritical']
        exclude_tag = ['notready']
        tagstatexclude = 'ID_*'
        if opts.is_jenkins:
            # run with Jenkins
            params = ParamsHandler()
            cases_path = params.cases_path
            plan_id = params.tcms_plan_id
            run_id = params.tcms_run_id
            tags = params.case_tags
            priorities = params.case_priorities
            run_id, case_ids = tcms.get_case_ids(plan_id, run_id, tags,
                                                 priorities, opts.is_tcms)
            other_variables = params.other_variables
            if len(case_ids) == 0:
                print "There's no case matching filter conditions"
                sys.exit(255)
            tag_case_id = ['ID_' + str(id) for id in case_ids]
            output_dir = params.result_path
            if opts.is_tcms:
                # run with Jenkins and TCMS
                listener = params.tcms_listener(plan_id, run_id)
                run(cases_path,
                    loglevel=log_level,
                    include=tag_case_id,
                    exclude=exclude_tag,
                    noncritical=noncritical,
                    tagstatexclude=tagstatexclude,
                    outputdir=output_dir,
                    variable=other_variables,
                    listener=listener)
            else:
                # run with Jenkins but without TCMS
                run(cases_path,
                    loglevel=log_level,
                    include=tag_case_id,
                    exclude=exclude_tag,
                    outputdir=output_dir,
                    noncritical=noncritical,
                    variable=other_variables,
                    tagstatexclude=tagstatexclude)
        else:
            # run without Jenkins
            if not opts.cases:
                raise UsageError("case path must be set with -c or --cases!")
            if not opts.plan_id:
                raise UsageError("plan id must be set with -p or --planid!")
            plan_id = opts.plan_id
            run_id = opts.run_id
            cases_path = opts.cases
            tags = opts.case_tags
            priorities = opts.case_priorities
            output_dir = opts.output_dir
            run_id, case_ids = tcms.get_case_ids(plan_id, run_id, tags,
                                                 priorities, opts.is_tcms)
            other_variables = opts.other_variables
            if len(case_ids) == 0:
                print "There's no case matching filter conditions"
                sys.exit(255)
            tag_case_id = ['ID_' + str(id) for id in case_ids]
            if opts.is_tcms:
                # run without Jenkins but with TCMS
                listener = 'robotx.core.listener.TCMSListener:%s:%s' \
                           % (plan_id, run_id)
                if not opts.plan_id:
                    raise UsageError("plan id must be set using -p/--planid!")
                run(cases_path,
                    loglevel=log_level,
                    include=tag_case_id,
                    exclude=exclude_tag,
                    noncritical=noncritical,
                    tagstatexclude=tagstatexclude,
                    outputdir=output_dir,
                    variable=other_variables,
                    listener=listener)
            else:
                # run without Jenkins and TCMS
                run(cases_path,
                    loglevel=log_level,
                    include=tag_case_id,
                    exclude=exclude_tag,
                    outputdir=output_dir,
                    noncritical=noncritical,
                    variable=other_variables,
                    tagstatexclude=tagstatexclude)
