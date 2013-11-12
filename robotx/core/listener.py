"""
RobotX Listener.

Integrate with Test Case Management System, such as, test-run creating.
result re-write.

Author: Xin Gao <fdumpling@gmail.com>
"""

import re

from robotx.core.nitrateclient import TCMS


class TCMSListener(object):
    """
    integrate with Test Case Management System,
    such as, test-run creating, case-run status updating,
    tests syntex checking ...

    $ pybot --loglevel DEBUG
         --listener listener.TCMSListener:8243:52490 keyword_driven.txt
    >>> import os
    >>> test_source = '/home/xin/tmp/RobotDemo/keyword_driven.txt'
    >>> cmd = 'pybot --listener listener.TCMSListener %s' % test_source
    >>> os.system(cmd)
    """
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, planid, runid):
        self.planid = planid
        self.runid = runid
        self.tcms = TCMS()
        self.tcms.update_run_status(self.runid, 0)
        self.caseruns = []

    def start_suite(self, name, attrs):
        """
        do sth when one test-suite start to run.
        long name is:  Suite1 & Suite2.Suite2.Invalid Login
        source:  /home/xin/tmp/WebDemo/suite2/invalid_login.txt
        """
        pass

    def start_test(self, name, attrs):
        """
        do sth when one case-run start to run.
        """
        caserun = {}
        caserun['name'] = name
        tags = attrs['tags']
        case_id = re.findall('ID_\d+|id_\d+', str(tags))[0][3:]
        caserun['id'] = self.tcms.get_caserun_id(self.runid, case_id)
        caserun['tags'] = tags
        caserun['status'] = 'RUNNING'
        caserun['starttime'] = attrs['starttime']
        # change tcms case status to RUNNING
        self.tcms.update_caserun_status(caserun['id'], caserun['status'])
        print '\n', '*' * 79
        print 'Start Running Time: ', caserun['starttime']
        self.caseruns.append(caserun)

    def end_test(self, name, attrs):
        """
        do sth when one case-run finish.
        """
        caserun = self.caseruns[-1]
        caserun['status'] = attrs['status']
        caserun['endtime'] = attrs['endtime']
        caserun['message'] = attrs['message']
        caserun['log'] = '\n' + '*' * 30 + '\n' + caserun['logtime'] + \
                         '\n' + attrs['message'] + '\n' + \
                         caserun['loginfo'] + '\n' + '*' * 30
        # change tcms case status to attrs['status'], PASS/FAIL
        caserun_status = caserun['status'] + 'ED'
        self.tcms.update_caserun_status(caserun['id'], caserun_status)
        if caserun['status'] != 'PASS':
            self.tcms.update_caserun_log(caserun['id'], caserun['log'])
        print 'End Running Time: ', caserun['endtime']
        print '*' * 79, '\n'

    def log_message(self, message):
        """
        do sth when one keyword error
        """
        if len(self.caseruns) > 0:
            caserun = self.caseruns[-1]
            caserun['loginfo'] = message['message']
            caserun['logtime'] = message['timestamp']
        else:
            pass

    def close(self):
        """
        do sth when all test-caseruns are end.
        """
        self.tcms.update_run_status(self.runid, 1)
        print '\n', 'AUTOMATION DONE'.center(70, '*'), '\n'
