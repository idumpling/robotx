RobotX
======

Instructions
------------
The RobotX is a tool set for automation development with [Robot Framework][Robot Framework].

It includes the following tools:
* Runner
* Generator
* Debugger
* Checker
* Expander

Installation
------------
    $ pip install robotx
    or
    $ easy_install robotx

Usage
-----
[RobotX Usage Doc][RobotX Usage]

Build & Config Jenkins
----------------------
[Build and Config Jenkins Doc][Build Config Jenkins]


Robot Framework Best Practices
------------------------------
[Robot Framework Best Practices Doc][Best Practice]

Test Case Management System
---------------------------
### Default TCMS Client   
Currently, RobotX uses [Nitrate][Nitrate] as default TCMS(Test Case Management System). If your TCMS is not Nitrate(such as TestLink), you need write a new client and replace the [default TCMS client of RobotX][nitrate client].

### Configure TCMS Client   
* Copy [config template file][tcms config] to /etc/, and name it as tcms.conf.
* Open tcms.conf, and change all values to yours.

Coming Soon
-----------
* Create Message Queue for improving the efficiency of RobotX communicate with TCMS.
* Add the mechanism of parallel execution automated cases on multiple machine nodes at one time.


[Robot Framework]: http://robotframework.org/
[RobotX Usage]: https://github.com/idumpling/robotx/blob/master/docs/USAGE.md
[Build Config Jenkins]: https://github.com/idumpling/robotx/blob/master/docs/JENKINS_CONFIG.md
[Best Practice]: https://github.com/idumpling/robotx/blob/master/docs/ROBOT_BEST_PRACTICE.md
[Nitrate]: https://fedorahosted.org/nitrate/
[nitrate client]: https://github.com/idumpling/robotx/blob/master/robotx/core/nitrateclient.py
[tcms config]: https://github.com/idumpling/robotx/blob/master/robotx/conf/tcms.conf
