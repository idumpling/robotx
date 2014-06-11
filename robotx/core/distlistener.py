"""Listener for testing running on multi slaves"""

import re
import zmq

from robotx.utils.misc import print_output


class MultiListener(object):
    """docstring for MultiListener"""

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, masterip, port):
        # create socket for sending tcms xmlrpc signal
        self.caserun = {}
        self.context = zmq.Context.instance()
        self.results_sender = self.context.socket(zmq.PUSH)
        self.sport = str(int(port) + 1)
        self.results_sender.connect("tcp://%s:%s" % (masterip, self.sport))

    def start_test(self, name, attrs):
        """do sth when testing start"""
        self.caserun['casename'] = name
        self.caserun['start_time'] = attrs['starttime']
        print_output(startend='start', starttime=self.caserun['start_time'],
                     msg=self.caserun['casename'])

    def end_test(self, name, attrs):
        """do sth when testing end"""
        tags = attrs['tags']
        self.caserun['caseid'] = re.findall('ID_\d+|id_\d+', str(tags))[0][3:]
        self.caserun['status'] = attrs['status'] + 'ED'
        self.caserun['end_time'] = attrs['endtime']
        self.caserun['message'] = attrs['message']
        if 'logtime' in self.caserun:
            self.caserun['log'] = '\n' + '*' * 30 + '\n' + \
                                  self.caserun['logtime'] + \
                                  '\n' + attrs['message'] + '\n' + \
                                  self.caserun['loginfo'] + '\n' + '*' * 30
        else:
            self.caserun['log'] = ''
        # change tcms case status to attrs['status'], PASS/FAIL
        print_output(startend='end', passfail=self.caserun['status'],
                     starttime=self.caserun['start_time'],
                     endtime=self.caserun['end_time'],
                     msg=self.caserun['casename'],
                     others=self.caserun['message'])
        self.results_sender.send_pyobj(self.caserun)

    def log_message(self, message):
        """do sth when one keyword error"""
        self.caserun['loginfo'] = message['message']
        self.caserun['logtime'] = message['timestamp']
