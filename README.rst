RobotX
======

Instructions
------------

The RobotX is a tool set for automation development with `Robot Framework`_.

It includes the following tools:

- Runner
- Generator
- Debugger
- Checker
- Expander

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

Currently, RobotX uses `Nitrate`_ as default TCMS(Test Case Management System). If your TCMS is not Nitrate(such as TestLink), you need write a new client and replace the `default TCMS client of RobotX`_.

Configure TCMS Client   
~~~~~~~~~~~~~~~~~~~~~

- Copy `tcms config`_ to /etc/, and name it as tcms.conf.

- Open tcms.conf, and change all values to yours.

Coming Soon
-----------

- Create Message Queue for improving the efficiency of RobotX communicate with TCMS.

- Add the mechanism of parallel execution automated cases on multiple machine nodes at one time.



.. _Robot Framework: http://robotframework.org/
.. _RobotX Usage Doc: https://github.com/idumpling/robotx/blob/master/docs/USAGE.md
.. _Build Config Jenkins: https://github.com/idumpling/robotx/blob/master/docs/JENKINS_CONFIG.md
.. _Robot Framework Best Practice: https://github.com/idumpling/robotx/blob/master/docs/ROBOT_BEST_PRACTICE.md
.. _Nitrate: https://fedorahosted.org/nitrate/
.. _default TCMS client of RobotX: https://github.com/idumpling/robotx/blob/master/robotx/core/nitrateclient.py
.. _tcms config: https://github.com/idumpling/robotx/blob/master/robotx/conf/tcms.conf
