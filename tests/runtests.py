""" RobotX Tests Trigger

This is for running all RobotX tests.

Usage: python runtests.py

"""

import os
import tempfile

from robot import run


def run_tests():
    test_path = os.path.curdir
    tmp_path = tempfile.gettempdir()
    output_dir = os.path.join(tmp_path, "robotx_test_result")
    os.mkdir(output_dir)
    output_file = os.path.join(output_dir, "output.xml")
    log_file = os.path.join(output_dir, "log.html")
    report_file = os.path.join(output_dir, "report.html")

    suites = ["test_cmd_*"]

    run(test_path,
        suite=suites,
        outputdir=output_dir,
        output=output_file,
        log=log_file,
        report=report_file)


if __name__ == '__main__':
    run_tests()
