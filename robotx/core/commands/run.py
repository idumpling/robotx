"""Sub command: run

Usage: robotx run [options]
"""


import os
import sys
from datetime import datetime
from multiprocessing import Pool

from robot import run

from robotx.core.base import BaseCommand
from robotx.core.nitrateclient import TCMS
from robotx.core.exceptions import UsageError
from robotx.core.paramshandler import ParamsHandler
from robotx.core.predistribute import collect_results
from robotx.core.predistribute import distribute_tasks
from robotx.core.predistribute import launch_workers


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
        parser.add_option('--distributed', action='store_true', dest='is_dist',
                          help='for distributed testing. \
                          default is running as no distributed.')
        parser.add_option('--jenkins', action='store_true', dest='is_jenkins',
                          help='Whether run project in jenkins. \
                          default is running in local.')
        parser.add_option('--tcms', action='store_true', dest='is_tcms',
                          help='Whether write result to tcms in real-time. \
                          default is running without tcms.')
        parser.add_option("-c", "--cases", dest="cases",
                          metavar="CASES_PATH", help="Set PROJECT Cases_PATH")
        parser.add_option("-m", "--masterip", dest="masterip",
                          metavar="MASTER_IP", help="Set MASTER_IP")
        parser.add_option("-p", "--planid", dest="plan_id",
                          metavar="PLAN_ID", help="Set PLAN_ID")
        parser.add_option("-r", "--runid", dest="run_id", default='',
                          metavar="RUN_ID", help="Set RUN_ID")
        parser.add_option("-o", "--output", dest="output_dir", default='./',
                          metavar="OUTPUT_DIR", help="Set OUTPUT_DIR")
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
        parser.add_option("-h", "--hosts", dest="slave_ips", action="append",
                          default=[], metavar="HOSTS",
                          help="Specify workers via ips")
        parser.add_option("-w", "--password", dest="password",
                          metavar="PASSWORD", help="Set worker PASSWORD")

    def run(self, args, opts):
        """Sub command 'run' runner"""
        stime = datetime.now()
        tcms = TCMS()
        log_level = 'DEBUG'
        noncritical = ['noncritical']
        exclude_tag = ['notready']
        tagstatexclude = 'ID_*'
        if opts.is_jenkins:
            # run with Jenkins
            params = ParamsHandler()
            project_name = params.project_name
            os.environ['project_name'] = project_name
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
            tag_case_id = ['ID_' + str(theid) for theid in case_ids]
            output_dir = params.result_path
            if not opts.is_dist:
                # In Jenkins, run all testing on one node, and not distributed
                if opts.is_tcms:
                    # run with Jenkins and TCMS
                    listener = params.tcms_listener(plan_id, run_id)
                    run(cases_path,
                        loglevel=log_level,
                        include=tag_case_id,
                        exclude=exclude_tag,
                        noncritical=noncritical,
                        outputdir=output_dir,
                        variable=other_variables,
                        tagstatexclude=tagstatexclude,
                        listener=listener)
                else:
                    # run with Jenkins but without TCMS
                    run(cases_path,
                        loglevel=log_level,
                        include=tag_case_id,
                        exclude=exclude_tag,
                        noncritical=noncritical,
                        outputdir=output_dir,
                        variable=other_variables,
                        tagstatexclude=tagstatexclude)
            else:
                # In Jenkins, running testing on multi nodes concurrently
                if not params.master_ip:
                    raise UsageError("mater ip must be set")
                if not params.slave_ips:
                    raise UsageError("slave ip must be set")
                if not params.slave_pwd:
                    raise UsageError("slave password must be set")
                slave_password = params.slave_pwd
                os.environ['all_slave_password'] = slave_password
                slavesip_list = params.slave_ips
                slavesip = reduce(lambda x, y: x + ',' + y, slavesip_list)
                masterip = params.master_ip
                worker_root = '/home/automation'
                project_path = params.project_path
                robotpool = Pool()
                print 'Start to launch workers ...'.center(50, '*')
                robotpool.apply_async(launch_workers,
                                      args=(project_path, worker_root,
                                            masterip, slavesip,
                                            plan_id, other_variables,))
                robotpool.apply_async(distribute_tasks,
                                      args=(tag_case_id, plan_id,))
                robotpool.apply_async(collect_results,
                                      args=(tag_case_id, plan_id, run_id,
                                            worker_root, slavesip,
                                            opts.is_tcms, output_dir))
                robotpool.close()
                robotpool.join()
        else:
            # run without Jenkins
            if not opts.cases:
                raise UsageError("case path must be set with -c or --cases!")
            if not opts.plan_id:
                raise UsageError("plan id must be set with -p or --planid!")
            plan_id = opts.plan_id
            run_id = opts.run_id
            project_path = opts.cases
            if project_path[-1] == '/':
                project_path = project_path[:-1]
            project_name = project_path.split('/')[-1]
            os.environ['project_name'] = project_name
            pass
            cases_path = os.path.join(project_path, 'cases')
            tags = opts.case_tags
            priorities = opts.case_priorities
            output_dir = opts.output_dir
            run_id, case_ids = tcms.get_case_ids(plan_id, run_id, tags,
                                                 priorities, opts.is_tcms)
            other_variables = opts.other_variables
            if len(case_ids) == 0:
                print "There's no case matching filter conditions"
                sys.exit(255)
            tag_case_id = ['ID_' + str(theid) for theid in case_ids]
            # In cmd, run all testing on one node, and not distributed.
            if not opts.is_dist:
                if opts.is_tcms:
                    # run without Jenkins but with TCMS
                    listener = 'robotx.core.listener.TCMSListener:%s:%s' \
                               % (plan_id, run_id)
                    run(cases_path,
                        loglevel=log_level,
                        include=tag_case_id,
                        exclude=exclude_tag,
                        noncritical=noncritical,
                        outputdir=output_dir,
                        variable=other_variables,
                        tagstatexclude=tagstatexclude,
                        listener=listener)
                else:
                    # run without Jenkins and TCMS
                    run(cases_path,
                        loglevel=log_level,
                        include=tag_case_id,
                        exclude=exclude_tag,
                        noncritical=noncritical,
                        outputdir=output_dir,
                        variable=other_variables,
                        tagstatexclude=tagstatexclude)
            # In cmd, running testing on multi nodes concurrently
            else:
                if not opts.masterip:
                    raise UsageError("mater ip must be set with -m")
                if not opts.slave_ips:
                    raise UsageError("slave ip must be set \
                        with -i or --slave_ips")
                if not opts.password:
                    raise UsageError("password must be set \
                        with -w or --password!")
                slave_password = opts.password
                os.environ['all_slave_password'] = slave_password
                slavesip_list = opts.slave_ips
                slavesip = reduce(lambda x, y: x + ',' + y, slavesip_list)
                masterip = opts.masterip
                worker_root = '/home/automation'
                robotpool = Pool()
                robotpool.apply_async(launch_workers,
                                      args=(project_path, worker_root,
                                            masterip, slavesip,
                                            plan_id, other_variables,))
                robotpool.apply_async(distribute_tasks,
                                      args=(tag_case_id, plan_id,))
                robotpool.apply_async(collect_results,
                                      args=(tag_case_id, plan_id, run_id,
                                            worker_root, slavesip,
                                            opts.is_tcms, output_dir,))
                robotpool.close()
                robotpool.join()
        etime = datetime.now()
        elapsed_time = etime - stime
        print 'Elapsed Time: %s' % elapsed_time
