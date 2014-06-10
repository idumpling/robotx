"""Functions for pre-distribute tasks to all workers"""


import os
import time

import zmq

import robotx


def launch_workers(project_path, worker_root, masterip,
                   slavesip, planid, other_variables):
    """docstring for launch_worker"""
    robotx_path = robotx.__path__[0]
    fab_file = os.path.join(robotx_path, 'core', 'fabworker.py')
    cases_path = os.path.join(project_path, 'cases')
    copyfiles = "copy_files:%s,%s" % (project_path, worker_root)
    runworkers = "run_workers:%s,%s,%s,%s,%s" \
        % (worker_root, masterip, planid, cases_path, other_variables)
    os.system("fab -f %s -H %s %s %s"
              % (fab_file, slavesip, copyfiles, runworkers))


def distribute_tasks(tags, port):
    """distribute all tasks to workers"""
    context = zmq.Context.instance()
    client = context.socket(zmq.ROUTER)
    client.bind("tcp://*:%s" % port)
    for tag in tags:
        # LRU worker is next waiting in the queue
        #worker_ip, empty, msg = client.recv_multipart()
        address, empty, msg = client.recv_multipart()
        if msg == 'Ready':
            print 'worker <%s> works well:-)' % address
        client.send_multipart([
            address,
            b'',
            tag,
        ])


def collect_results(tags, port, worker_root, slavesip, is_tcms):
    """for collecting tcms xmlrpc signal and dealing with them"""
    context = zmq.Context()
    # socket for results_receive
    results_receiver = context.socket(zmq.PULL)
    rport = str(int(port) + 1)
    results_receiver.bind("tcp://*:%s" % rport)
    task_num = len(tags)
    receive_count = 0
    # socket for worker control(send kill signal)
    controller = context.socket(zmq.PUB)
    cport = str(int(port) - 1)
    controller.bind("tcp://*:%s" % cport)
    while True:
        result = results_receiver.recv_pyobj()
        receive_count += 1
        print '######################the content is: ', result
        print '######################receive_count is: ', receive_count
        if is_tcms:
            #***************** Update TCMS caserun status **************
            print 'emulate tcms doing'.center(80, '*')
            print 'the content is: ', result
            time.sleep(5)
            #receive_count += 1
            print 'tcms well done'.center(80, '*')
            #*********************** Finally ***************************
        if receive_count == task_num:
            #sending kill signal to workers
            controller.send_pyobj("KILL")
            # collect reports and produce final report
            robotx_path = robotx.__path__[0]
            fab_file = os.path.join(robotx_path, 'core', 'fabworker.py')
            collectresults = "collect_reports:%s" % worker_root
            os.system("fab -f %s -H %s %s"
                      % (fab_file, slavesip, collectresults))
            os.system("rebot --name 'Demo Report' --output alloutput \
                      --log alllog --report allreport \
                      --processemptysuite --tagstatexclude 'ID_*' ./*.xml")
            # kill all!!!
            time.sleep(5)
            break
    print '\n', 'GAME OVER'.center(80, '=')


if __name__ == '__main__':
    TAGS = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']
            #'tag6', 'tag7', 'tag8', 'tag9', 'tag10']
    PLANID = '10771'
    distribute_tasks(tags=TAGS, port=PLANID)
