"""Listener for testing running on multi slaves"""

import zmq

from robotx.utils.misc import print_output


class MultiListener(object):
    """docstring for MultiListener"""

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, masterip, port):
        # create socket for sending tcms xmlrpc signal
        self.context = zmq.Context.instance()
        self.results_sender = self.context.socket(zmq.PUSH)
        self.sport = str(int(port) + 1)
        self.results_sender.connect("tcp://%s:%s" % (masterip, self.sport))

    def start_test(self, name, attrs):
        """do sth when testing start"""
        testing_name = name
        start_time = attrs['starttime']
        print_output(startend='start', starttime=start_time, msg=testing_name)

    def end_test(self, name, attrs):
        """do sth when testing end"""
        testing_name = name
        result_status = attrs['status']
        start_time = attrs['starttime']
        end_time = attrs['endtime']
        message = attrs['message']
        print_output(startend='end', passfail=result_status,
                     starttime=start_time,endtime=end_time,
                     msg=testing_name, others=message)
        self.results_sender.send_pyobj(testing_name)




