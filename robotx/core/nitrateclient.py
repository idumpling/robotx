"""
RobotX TCMS Client

TCMS means Test Case Management System.

Currently, RobotX uses Nitrate as default TCMS.
If your TCMS is not Nitrate(such as TestLink)
you need write a new client and replace the default TCMS client of RobotX.

Author: Xin Gao <fdumpling@gmail.com>
"""

import os
import sys
import time
import logging
import pexpect
import kerberos
import ConfigParser

from nitrate import NitrateKerbXmlrpc


class TCMS(object):
    """TCMS client
    """

    def __init__(self, tcms_url=None):
        self.log = logging.getLogger()
        # kerberos login
        if tcms_url is None:
            self.tcms_url = self.get_tcms_url()
        else:
            self.tcms_url = tcms_url
        try:
            self.server = NitrateKerbXmlrpc(self.tcms_url).server
        except kerberos.GSSError:
            print 'Nitrate login ...'
            self.user = os.environ.get('TCMS_LOGIN_NAME')
            self.passwd = os.environ.get('TCMS_LOGIN_PWD')
            self.kinit(self.user, self.passwd)
            print "Successfully Kinit"
            self.server = NitrateKerbXmlrpc(self.tcms_url).server

    def _config_setting(self):
        """for getting conf file value"""
        config = ConfigParser.ConfigParser()
        config.read('/etc/tcms.conf')
        return config

    def get_tcms_url(self):
        """As subject~"""
        config = self._config_setting()
        try:
            env = config.get('TCMS', 'environment')
            url = config.get('TCMS', env)
        except ConfigParser.NoSectionError:
            raise TCMSException("ERROR[TCMS]': \
                  pls check/update /etc/tcms.conf file")
        return url

    def get_domain(self):
        """As subject~"""
        config = self._config_setting()
        try:
            domain_name = config.get('TCMS', 'domain')
        except ConfigParser.NoSectionError:
            raise TCMSException("ERROR[TCMS]': \
                  pls check/update /etc/tcms.conf file")
        return domain_name

    def kinit(self, user, passwd):
        """Do kinit ops for the kerberos authentication"""
        domain_name = self.get_domain()
        try:
            kinit = pexpect.spawn('kinit %s' % user)
            kinit.expect('Password for %s@%s:' % (user, domain_name))
            print kinit.after
            kinit.sendline(passwd)
            index = kinit.expect([pexpect.EOF, pexpect.TIMEOUT])
            print index, kinit.before
        except pexpect.EOF:
            print "\nFailed to login, you need Do kinit firstly!!!"
            sys.exit(255)

    def get_caserun_id(self, run_id, case_id):
        """for getting case run id
        """
        caseruns = self.server.TestCaseRun.filter(
            {'run__run_id': run_id, 'case__case_id': case_id})
        caserun_id = caseruns[0]['case_run_id']
        return caserun_id

    def get_caserun_status_id(self, status):
        """for getting case run status id.
        status = {
            'IDEL': 1,
            'PASSED': 2,
            'FAILED': 3,
            'RUNNING': 4,
            'PAUSED': 5,
            'BLOCKED': 6,
            'ERROR': 7,
            'WAIVED': 8,
        }
        """
        caserun_status = self.server.\
            TestCaseRun.check_case_run_status(status)
        return caserun_status['id']

    def update_caserun_status(self, caserun_id, caserun_status):
        """for updating case-run status
        """
        caserun_status_id = self.get_caserun_status_id(caserun_status)
        self.server.TestCaseRun.update(
            caserun_id, {'case_run_status': caserun_status_id})

    def update_caserun_log(self, caserun_id, caserun_log):
        """for updating case-run log to comment
        """
        self.server.TestCaseRun.add_comment(caserun_id, caserun_log)

    def get_run_params(self, plan_id, case_ids):
        """get params for creating new run.
        """
        # get summary, required
        create_time = time.strftime('%Y-%m-%d %X', time.localtime())
        product_name = self.server.TestPlan.get(plan_id)['product']
        run_summary = product_name + '_' + 'automation' + '_' + create_time
        # get mananger id, requied
        run_manager = self.server.TestPlan.get(plan_id)['owner_id']
        # get product id, required
        run_product = self.server.TestPlan.get(plan_id)['product_id']
        # get product version id, required
        run_product_version = \
            self.server.TestPlan.get(plan_id)['product_version_id']
        # get build id, required
        run_build = self.server.Product.get_builds(run_product)[0]['build_id']
        # get plan id
        run_plan_id = plan_id
        run_values = {
            'summary': run_summary,
            'manager': run_manager,
            'product': run_product,
            'product_version': run_product_version,
            'build': run_build,
            'plan': run_plan_id,
            'case': case_ids,
        }
        return run_values

    def create_run(self, plan_id, tags, priorities):
        """create new test run in TCMS
        """
        run_values = {}
        case_ids = self.get_valid_cases(plan_id, tags, priorities)
        run_values = self.get_run_params(plan_id, case_ids)
        try:
            self.log.debug("Create run ...")
            run_id = self.server.TestRun.create(run_values)['run_id']
            self.log.info("Run %s was successfully created." % (run_id))
            return run_id
        except Exception as e:
            raise TCMSException("ERROR[TCMS]: Couldn't create TestRun(%s) :: \
                %s" % (str(run_values), str(e)))

    def add_cases_to_run(self, cases_ids, run_id):
        """add case
        """
        exist_cases = self.server.TestRun.get_test_cases(run_id)
        exist_cases_ids = [case['case_id']for case in exist_cases]
        if type(cases_ids) == str or type(cases_ids) == int:
            if int(cases_ids) in exist_cases_ids:
                new_caserun_count = 0
            else:
                new_caserun_count = 1
        elif type(cases_ids) == list:
            new_cases_ids = [id for id in cases_ids
                             if int(id) not in exist_cases_ids]
            new_caserun_count = len(new_cases_ids)
        else:
            pass
        if new_caserun_count > 0:
            try:
                self.server.TestCase.add_to_run(cases_ids, run_id)
            except Exception, error_info:
                self.log.warning('detail info: \n %s' % error_info)
        else:
            pass

    def get_case_from_run(self, run_id):
        """for getting case list from run.
        """
        try:
            return self.server.TestRun.get_test_cases(run_id)
        except:
            raise TCMSException("ERROR[TCMS]': \
                Failed to get testcases for testrun %s" % str(run_id))

    def update_run_status(self, run_id, status_num):
        """for update run status to FINISHED or RUNNING
        """
        try:
            self.server.TestRun.update(run_id, {'status': status_num})
        except:
            raise TCMSException("ERROR[TCMS]': Failed to update run status")

    def get_valid_cases(self, plan_id, tags, priorities):
        """for get case ids via plan id and tags
        """
        cases = []
        tags_cases = self.get_valid_cases_via_tags(plan_id, tags)
        priorities_cases = self.get_valid_cases_via_priorities(plan_id,
                                                               priorities)
        cases = [case for case in tags_cases if case in priorities_cases]
        return cases

    def get_valid_cases_via_tags(self, plan_id, tags):
        """for getting case ids via plan id and tags
        """
        cases = []
        if len(tags) == 0:
            try:
                the_cases = self.server.TestCase.filter({
                    'plan__plan_id': plan_id,
                    'is_automated': 1,
                    'case_status__name': 'CONFIRMED'
                    })
            except:
                raise TCMSException("ERROR[TCMS]': \
                        Failed to filter case")
            else:
                cases = [case['case_id'] for case in the_cases]
        else:
            for tag in tags:
                try:
                    the_cases = self.server.TestCase.filter({
                        'plan__plan_id': plan_id,
                        'is_automated': 1,
                        'case_status__name': 'CONFIRMED',
                        'tag__name': tag
                        })
                except:
                    raise TCMSException("ERROR[TCMS]': \
                            Failed to filter case")
                else:
                    cases1 = [case['case_id'] for case in the_cases]
                    cases = list(set(cases1 + cases))
        return cases

    def get_valid_cases_via_priorities(self, plan_id, priorities):
        """for getting case ids via plan id and priorities
        """
        cases = []
        if len(priorities) == 0:
            try:
                the_cases = self.server.TestCase.filter({
                    'plan__plan_id': plan_id,
                    'is_automated': 1,
                    'case_status__name': 'CONFIRMED'
                    })
            except:
                raise TCMSException("ERROR[TCMS]': \
                        Failed to filter case")
            else:
                cases = [case['case_id'] for case in the_cases]
        else:
            for priority in priorities:
                try:
                    the_cases = self.server.TestCase.filter({
                        'plan__plan_id': plan_id,
                        'is_automated': 1,
                        'case_status__name': 'CONFIRMED',
                        'priority__value': priority.upper()
                        })
                except:
                    raise TCMSException("ERROR[TCMS]': \
                            Failed to filter case")
                else:
                    cases1 = [case['case_id'] for case in the_cases]
                    cases = list(set(cases1 + cases))
        return cases

    def get_plan_case_ids(self, plan_id):
        """return case id list via plan id
        """
        case_ids = []
        cases = self.server.TestPlan.get_test_cases(plan_id)
        case_ids = [case['case_id'] for case in cases]
        return case_ids

    def get_case_ids(self, plan_id, run_id, tags, priorities, is_tcms):
        """return specified and automated case ids
        """
        case_ids = []
        if is_tcms:
            if run_id == '':
                if plan_id == '':
                    print 'Plan ID is required option!!!'
                    sys.exit(255)
                else:
                    run_id = self.create_run(plan_id, tags, priorities)
                    print '\n', 'New Run ID: %s'.center(70, '*') % run_id, '\n'
                    cases = self.get_case_from_run(run_id)
                    case_ids = [case['case_id'] for case in cases]
            else:
                cases_in_run = self.get_case_from_run(run_id)
                case_ids_in_run = [case['case_id'] for case in cases_in_run]
                valid_case_ids = self.get_valid_cases(plan_id, tags,
                                                      priorities)
                case_ids = [id for id in case_ids_in_run
                            if id in valid_case_ids]
                print '\n', 'Existing Run ID: %s'.center(70, '*') % run_id
                print '\n'
        elif plan_id == '':
            print 'Plan ID is required option!!!'
            sys.exit(255)
        else:
            case_ids = self.get_valid_cases(plan_id, tags, priorities)
        return str(run_id), case_ids


class TCMSException(Exception):
    """General tcms exception"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


if __name__ == '__main__':
    tcms = TCMS()
    run_id = 52489
    case_id = 154226
    caserun_id = 1824331
    plan_id = 8243
    caserun_log = """
    Traceback (most recent call last):
    File "/home/xin/tmp/robotdemo/CalculatorLibrary.py",
    line 26, in push_button
    self._result = self._calc.push(button)
    File "/home/xin/tmp/robotdemo/calculator.py", line 9, in push
    raise CalculationError("Invalid button '%s'." % button)
    """
    # test get_caserun_id()
    # caserun_id = tcms.get_caserun_id(run_id, case_id)
    # print 'Case-run-id is: ', caserun_id

    # test update_caserun_status()
    # caserun_status = 'RUNNING'
    # tcms.update_caserun_status(1865655, caserun_status)

    # test update_caserun_log()
#    tcms.update_caserun_log(caserun_id, caserun_log)

    # test create_run()
#    run_id = tcms.create_run(plan_id)
#    print 'run_id is: ', run_id
#    tcms.add_case_to_run(198676, 52489)
    # tags = ['[Local Time]']
    # priorities = []
    # run_id, cases = tcms.get_case_ids(8342, '', tags, priorities, 0)
    # print cases, run_id
#    tcms.update_run_status('80792', 1)
