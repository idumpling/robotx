"""fabric ops"""


import os

from fabric.api import cd
from fabric.api import env
from fabric.api import get
from fabric.api import put
from fabric.api import run
from fabric.api import shell_env

import robotx


# env.user = 'root'
env.password = os.environ['all_slave_password']
# env.hosts = ['192.168.122.56', '192.168.122.153', '192.168.122.254']

env.skip_bad_hosts = True
#env.timeout=120
env.parallel = True


def copy_files(project_path, worker_root):
    """copy all needed files to workers"""
    # send tests file to worker
    robotx_path = robotx.__path__[0]
    worker_file = os.path.join(robotx_path, 'core', 'workerdaemon.py')
    put(project_path, worker_root, use_sudo=True)
    put(worker_file, worker_root, use_sudo=True)


def run_workers(worker_root, masterip, planid, project_name, other_variables):
    """run all workers on given hosts"""
    worker_file = 'workerdaemon.py'
    worker_cmd = 'python %s %s %s %s %s' \
        % (worker_file, masterip, planid, project_name, other_variables)
    with shell_env(DISPLAY=':0'):
        with cd(worker_root):
            run(worker_cmd)


def collect_reports(worker_root, project_name):
    """docstring for collect_reports"""
    results_path = os.path.join(worker_root, project_name, 'results')
    with cd(results_path):
        print "\nStart to collect result files"
        get('*.xml', './')
        run('rm -rf *.xml')
