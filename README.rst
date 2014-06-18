RobotX
======

Instructions
------------

**Let all your robot Framework test cases fly!**

The RobotX is a tool set for automation development with `Robot Framework`_.

The Newest version (since version 0.2.1) can automatically intelligently and dynamically  
partition all automated tests into multiple pcs, and each one of which can be  
executed in parallel.
The execution can happen on different physical/virtual machines.
More the partitions, less tests executed on each one.
That means that if you have multiple pcs you can use them for a combined test run.

And since all of the partitions start almost at the same time overall test-execution time 
gets divided by the number of partitions you make.
for the usage examples of distributed execution, refer to here.

- `Jenkins configure about distributed run`_

- `Parallel run in jenkins`_

- `Parallel run in cmd`_

It includes the following tools:

- Runner

- Generator

- Debugger

- Checker

- Expander

RobtX Runner is pretty powerful

- It can be integrated into Jenkins.  

- It can be used in command line.   

- It can be used to run tests in parallel (since version 0.2.1).  

- Get and filter tests from Test Case Management System.

- Executed tests can be filtered and collected from Test Case Management System.  

- The tests result can be updated to Test Case Management System in real-time.


Installation
------------

.. code:: bash

    $ pip install robotx
    or
    $ easy_install robotx


Usage
-----

`RobotX Usage Doc`_

Build & Config Jenkins
----------------------

`Build Config Jenkins`_


Robot Framework Best Practices
------------------------------

`Robot Framework Best Practice`_

Test Case Management System
---------------------------

Default TCMS Client  
~~~~~~~~~~~~~~~~~~~

Currently, RobotX uses `Nitrate`_ as default TCMS(Test Case Management System). 
If your TCMS is not Nitrate(such as TestLink), you need write a new client and replace the `default TCMS client of RobotX`_.

Configure TCMS Client   
~~~~~~~~~~~~~~~~~~~~~

- Copy `tcms config`_ to /etc/, and name it as tcms.conf.

- Open tcms.conf, and change all values to yours.



.. _Robot Framework: http://robotframework.org/
.. _RobotX Usage Doc: https://github.com/idumpling/robotx/blob/master/docs/USAGE.md
.. _Build Config Jenkins: https://github.com/idumpling/robotx/blob/master/docs/JENKINS_CONFIG.md
.. _Robot Framework Best Practice: https://github.com/idumpling/robotx/blob/master/docs/ROBOT_BEST_PRACTICE.md
.. _Nitrate: https://fedorahosted.org/nitrate/
.. _default TCMS client of RobotX: https://github.com/idumpling/robotx/blob/master/robotx/core/nitrateclient.py
.. _tcms config: https://github.com/idumpling/robotx/blob/master/robotx/conf/tcms.conf
.. _Jenkins configure about distributed run: https://github.com/idumpling/robotx/blob/master/docs/JENKINS_CONFIG.md#parameters-for-running-as-distributed  
.. _Parallel run in jenkins: https://github.com/idumpling/robotx/blob/master/docs/JENKINS_CONFIG.md#parallel-run-tests-on-more-than-one-pc  
.. _Parallel run in cmd: https://github.com/idumpling/robotx/blob/master/docs/USAGE.md#parallel-run-tests-on-more-than-one-pc  


