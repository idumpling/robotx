"""Functions for pre-distribute tasks to all workers"""


import os
import time

import zmq

import robotx
from robotx.core.nitrateclient import TCMS


def launch_workers(project_path, worker_root, masterip,
                   slavesip, planid, other_variables):
    """docstring for launch_worker"""
    print 'Start to launch workers ...'.center(50, '*')
    if project_path[-1] == '/':
        project_path = project_path[:-1]
    project_name = project_path.split('/')[-1]
    robotx_path = robotx.__path__[0]
    fab_file = os.path.join(robotx_path, 'core', 'fabworker.py')
    #cases_path = os.path.join(project_path, 'cases')
    #cases_path = os.path.join(project_name, 'cases')
    #results_path = os.path.join(project_name, 'results')
    copyfiles = "copy_files:%s,%s" % (project_path, worker_root)
    runworkers = "run_workers:%s,%s,%s,%s,%s" \
        % (worker_root, masterip, planid, project_name, other_variables)
    os.system('fab --hide=running -f %s -H %s %s'
              % (fab_file, slavesip, copyfiles))
    os.system('fab -f %s -H %s %s'
              % (fab_file, slavesip, runworkers))


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


def collect_results(tags, plan_id, run_id, worker_root, slavesip,
                    is_tcms, output_dir):
    """for collecting tcms xmlrpc signal and dealing with them"""
    project_name = os.environ['project_name']
    port = plan_id
    tcms = TCMS()
    tcms.update_run_status(run_id, 0)
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
        if is_tcms:
            #***************** Update TCMS caserun status **************
            caserun_id = tcms.get_caserun_id(run_id, result['caseid'])
            tcms.update_caserun_status(caserun_id, result['status'])
            if result['status'] != 'PASSED':
                tcms.update_caserun_log(caserun_id, result['log'])
            print 'Case-run %s is updated in TCMS' % result['caseid']
            #***********************************************************
        #*********************** Finally *******************************
        if receive_count == task_num:
            #sending kill signal to workers
            controller.send_pyobj("KILL")
            # collect reports and produce final report
            robotx_path = robotx.__path__[0]
            fab_file = os.path.join(robotx_path, 'core', 'fabworker.py')
            collectresults = "collect_reports:%s,%s" \
                % (worker_root, project_name)
            os.system('fab --hide=running -f %s -H %s %s'
                      % (fab_file, slavesip, collectresults))
            os.system("rebot --name 'RobotX Report' --outputdir %s \
                      --output output --processemptysuite --tagstatexclude \
                      'ID_*' ./*.xml" % output_dir)
            time.sleep(3)
            os.system('rm -rf ID_*.xml')
            # kill all workers!!!
            # coon die henchman boil:-)
            time.sleep(5)
            break
    tcms.update_run_status(run_id, 1)
    print '\n', 'GAME OVER'.center(80, '=')


if __name__ == '__main__':
    TAGS = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']
            #'tag6', 'tag7', 'tag8', 'tag9', 'tag10']
    PLANID = '10771'
    distribute_tasks(tags=TAGS, port=PLANID)
