"""
RobotX Checker Handler.

Currently class 'ResultVistor' is mainly used to
tests syntex and format checking.

But acctually it also can be used to deal with all tests result.

Author: Xin Gao <fdumpling@gmail.com>
"""

import re

from robot.api import ResultVisitor


class ResultChecker(ResultVisitor):
    """For tests format checking
    1. Make sure that the format of test name like 'Case 1234 ...',
       and verify that case id is included in the test plan.
    2. Make sure that test tags include tag 'ID_1234',
       and verify that case id is included in the test plnan.
    """

    def __init__(self, case_ids, plan_id):
        self.case_ids = case_ids
        self.plan_id = plan_id

    def visit_test(self, test):
        """Tests format checking func.

        test attrs including:
        test.name, test.status, test.message,
        test.doc, test.tags, test.timeout
        test.starttime, test.endtime
        """
        name_error = name_validate(test.name, self.case_ids, self.plan_id)
        tag_error = tag_validate(test.tags, self.case_ids, self.plan_id)
        if test.status == 'FAIL' or (name_error is not None) \
           or (tag_error is not None):
            print '=' * 79
            print '| FAIL |: ', test.name
            print '-' * 79
            if test.status == 'FAIL':
                print test.message
            if name_error is not None:
                print name_error
            if tag_error is not None:
                print tag_error
            print '=' * 79, '\n'


class DryRunChecker(ResultVisitor):
    """For tests syntex checking"""

    def __init__(self):
        pass

    def visit_test(self, test):
        """
        Just print the fail case info
        """
        if test.status == 'FAIL':
            print '=' * 79
            print '| FAIL |: ', test.name
            print '-' * 79
            print test.message
            print '=' * 79, '\n'


def name_validate(name, case_ids, plan_id):
    """Tests name checking func"""
    error_msg = None
    name_format = name.strip().split()
    if (name_format[0].lower() != 'case') or (not name_format[1].isdigit()):
        error_msg = "Wrong Case Name Format:\
                \nPls use 'Case case_id' as the beginning of automated name"
    elif int(name_format[1]) not in case_ids:
        error_msg = "Wrong Case ID:\
                \ncase %s doesn't belong to plan %s" \
                % (name_format[1], plan_id)
    return error_msg


def tag_validate(tags, case_ids, plan_id):
    """Tests tag checking func"""
    error_msg = None
    tag_id = re.findall('ID_\d+|id_\d+', str(tags))
    if not tag_id:
        error_msg = "Wrong Tag Format:\
                \nPls add tag 'ID_case_id' to this case."
    elif int(tag_id[0][3:]) not in case_ids:
        error_msg = "Wrong Tag Format:\
                \ncase %s don't belong to plan %s" % (tag_id[0][3:], plan_id)
    return error_msg
