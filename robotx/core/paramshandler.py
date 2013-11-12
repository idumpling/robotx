"""
RobotX parameters Handler.

Getting and Updating parameters.

Author: Xin Gao <fdumpling@gmail.com>
"""

import os
import sys
import logging


CUR_DIR = os.path.abspath(os.path.curdir)


class ParamsHandler(object):
    """For handling all parameters.

    handler = ParamsHandler()

    print 'plan id is: ', handler.tcms_plan_id
    print 'run id is: ', handler.tcms_run_id
    tags = handler.case_tags
    print tags
    listener = handler.tcms_listener
    print 'listener is: ', listener
    """
    def __init__(self):
        self.log = logging.getLogger()
        self.init_params()

    def init_params(self):
        """parameters initialazation
        """
        self.config = DotDict()
        self.param_list = ['PROJECT_NAME',
                           'TCMS_LOGIN_NAME',
                           'TCMS_LOGIN_PWD',
                           'TCMS_PLAN_ID',
                           'TCMS_RUN_ID',
                           'CASE_PRIORITIES',
                           'CASE_TAGS',
                           'OTHER_VARIABLES']
        for param in self.param_list:
            setattr(self.config, param.lower(), os.environ.get(param))

    @property
    def cases_path(self):
        """return case path
        """
        return os.path.join(CUR_DIR, 'tests',
                            self.config.project_name, 'cases')

    @property
    def result_path(self):
        """return result path
        """
        return os.path.join(CUR_DIR, 'tests',
                            self.config.project_name, 'results')

    @property
    def tcms_login_name(self):
        """return tcms login name
        """
        return self.config.tcms_login_name

    @property
    def tcms_login_pwd(self):
        """return tcms login password
        """
        return self.config.tcms_login_pwd

    @property
    def tcms_plan_id(self):
        """return plan id
        """
        if self.config.tcms_plan_id is None:
            print 'The TCMS_PLAN_ID is required parameters!!'
            sys.exit(255)
        else:
            return self.config.tcms_plan_id

    @property
    def tcms_run_id(self):
        """return run id
        """
        if self.config.tcms_run_id is None:
            self.config.tcms_run_id = ''
        return self.config.tcms_run_id

    @property
    def case_tags(self):
        """return a tag list
        """
        tags = []
        if self.config.case_tags is None:
            return tags
        else:
            tags_inital = self.config.case_tags.splitlines()
            tags = [tag.strip() for tag in tags_inital if tag.strip() != '']
            return tags

    @property
    def case_priorities(self):
        """return a priorities list
        """
        priorities = []
        if self.config.case_priorities is None:
            return priorities
        else:
            priorities_inital = self.config.case_priorities.splitlines()
            priorities = [priority.strip() for priority in priorities_inital
                          if priority.strip() != '']
            return priorities

    @property
    def other_variables(self):
        """return other variables list
        """
        variables = []
        if self.config.other_variables is None:
            return variables
        else:
            variables_inital = self.config.other_variables.splitlines()
            variables = [variable.strip() for variable in variables_inital
                         if variable.strip() != '']
            valid_variables = []
            for variable in variables:
                split = variable.find(":")
                if split == -1:
                    print "The format of variable %s is wrong!" % variable
                    sys.exit(255)
                if variable[split + 1] == " ":
                    variable = variable[:(split + 1)] + variable[(split + 2):]
                    valid_variables.append(variable)
                else:
                    valid_variables.append(variable)
            return valid_variables

    def tcms_listener(self, plan_id, run_id):
        """return like: "pathtolistener.yourlistener:'8243':'1234'"
        """
        listener_path = 'robotx.core.listener'
        listener = '%s.TCMSListener:%s:%s' % (listener_path, plan_id, run_id)
        return listener


class DotDict(object):

    def __getattr__(self, name):
        return self.data[name]

    def __setattr__(self, name, value):
        if not ('data' in self.__dict__):
            self.__dict__['data'] = {}
        self.__dict__['data'][name] = value
