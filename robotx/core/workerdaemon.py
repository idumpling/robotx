"""Distributed Testing System - Worker"""


import os
import sys
from random import randint

import zmq
from robot import run


def worker_shop(context=None, masterip='localhost', port='', project_name='',
                other_variables=''):
    """worker will say hi with task controller"""
    tests = os.path.join(project_name, 'cases')
    results_path = os.path.join(project_name, 'results')
    #worker_ip = get_ip()
    listener = 'robotx.core.distlistener.MultiListener:%s:%s' \
               % (masterip, port)
    #identity = unicode(worker_ip)
    identity = u"%04x-%04x" % (randint(0, 0x10000), randint(0, 0x10000))
    context = context or zmq.Context.instance()
    # socket for running task
    worker = context.socket(zmq.REQ)
    # We use a string identity for ease here
    #zhelpers.set_id(worker)
    worker.setsockopt_string(zmq.IDENTITY, identity)
    worker.connect("tcp://%s:%s" % (masterip, port))
    # socket for control input
    controller = context.socket(zmq.SUB)
    cport = str(int(port) - 1)
    controller.connect("tcp://%s:%s" % (masterip, cport))
    controller.setsockopt(zmq.SUBSCRIBE, b"")
    # Process messages from maskter and controller
    poller = zmq.Poller()
    poller.register(worker, zmq.POLLIN)
    poller.register(controller, zmq.POLLIN)
    while True:
        # Tell the router we're ready for work
        worker.send('Ready')
        socks = dict(poller.poll())
        if socks.get(worker) == zmq.POLLIN:
            # Get workload from router, until finished
            tag = worker.recv()
            #print '\nthe tag name is: %s\n' % tag
            with open('/tmp/stdout.txt', 'w') as stdout:
                run(tests,
                    loglevel='TRACE',
                    include=tag,
                    #exclude=['notready'],
                    noncritical=['noncritical'],
                    outputdir=results_path,
                    output=tag,
                    variable=other_variables,
                    tagstatexclude='ID_*',
                    listener=listener,
                    stdout=stdout,
                    runemptysuite=True)
        # Any waiting controller command acts as 'KILL'
        if socks.get(controller) == zmq.POLLIN:
            break


if __name__ == '__main__':
    THEARGS = sys.argv
    MASTERIP = THEARGS[1]
    PLANID = THEARGS[2]
    TESTS = THEARGS[3]
    OVARIABLES = THEARGS[4]
    worker_shop(masterip=MASTERIP, port=PLANID, project_name=TESTS,
                other_variables=OVARIABLES)
