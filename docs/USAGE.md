RobotX Usage
============

The RobotX is a tool set for automation development with [Robot Framework][Robot Framework].

The Newest version (since version 0.2.1) can automatically intelligently and dynamically  
partition all automated tests into multiple pcs, and each one of which can be  
executed in parallel.
The execution can happen on different physical/virtual machines.
More the partitions, less tests executed on each one.
That means that if you have multiple pcs you can use them for a combined test run.

And since all of the partitions start almost at the same time overall test-execution time 
gets divided by the number of partitions you make.
for the usage examples of distributed execution, refer to here.


Helper
------
#### Get all tools usage info  
    $ robotx --help  

#### Get single tool usage info  
    $ robotx run --help


Runner
------
### Run with jenkins  
#### Re-write tests info and result to TCMS(Test Case Management System)
Type cmd to Jenkins "Execute Shell" below  

    $ robotx run --jenkins --tcms

#### Do not re-write anything to TCMS  
Type cmd to Jenkins "Execute Shell" below  

    $ robotx run --jenkins

### Run without jenkins  
#### Re-write tests info and result to TCMS  
Type cmd to shell below

    $ robotx run --tcms --cases=CASES_PATH \  
      --planid=PLAN_ID --runid=RUN_ID --output=OUTPUT_DIR \  
      --tags=CASE_TAG --priorities=CASE_PRIORITY --variable=OTHER_VARIABLE  

**NOTE:**  
* --runid can be ignored, if ignored, RobotX will create new test run in TCMS  
* --output can be ignored, if ignored, all output files will be placed in current path.  
* --tags can be ignored, if ignored, RobotX will not filter case by tag.  
* --priorities can be ignored, if ignored, RobotX will not filter case by priority.  
* --variable can be ignored, if ignored, no variable can be change when run tests.  

#### Do not re-write anything to TCMS  
Type cmd to shell below  

    $ robotx run --cases=CASES_PATH --planid=PLAN_ID   

### Parallel run tests on more than one PC   
If you want to run all automated tests in parallel, you only need to add one addition 
argument "--distributed" on the nun-parallel basis.

### Parallel run with jenkins  
For the parallel running way in Jenkins, you need to make sure that following  three special 

parameters have been created and configured.   
* MASTER_IP   
* SLAVE_IPS   
* SLAVE_PWD   
for the detail steps, you can refer to this doc.    

for example,   

    $ robotx run --jenkins --tcms --distributed
    or   
    $ robotx run --jenkins --distributed

### Parallel run without jenkins   
Run tests from the command line.   
Besides the addition argument "--distributed" that you need to set up with, 
you need to set up following three arguments.   
* MASTER_IP   
* SLAVE_IPS   
* SLAVE_PWD   

for example,   

    $ robotx run --tcms --distributed --masterip='10.66.136.111' \    
      --planid='11340' --runid='149111' --cases='./Demo' \   
      --hosts='root@10.66.136.112' --hosts='root@10.66.136.113' \   
      --password='123456'   

**NOTE:**  
For the parallel running way, you need to make sure that following three addition 
python packages have been installed successfully in your master machine and all slaves machine. 
* pyzmq
* fabric
* netifaces

Previous experience suggested this route could be tricky to install the python package "pyzmq".  
If the process is failed via easy_install or python pip, you can try following steps,   
In Red Hat Enterprise Linux, CentOS, Fedora cases,

    $ yum groupinstall 'Development Tools'
    $ yum install python-devel
    $ yum install -y uuid-devel
    $ yum install -y pkgconfig
    $ yum install -y libtool
    $ yum install -y gcc-c++ 
    $ easy_install pip
    $ pip install pyzmq

Additionally, you'd better delete iptables rules on master machine.  

    $ iptables -F 


Generator
---------
### Generate new project using Template  
    $ robotx generate --project=PROJECT_NAME  

### Generate new suite file using Template  
    $ robotx generate --suite=SUITE_NAME  

### Generate new resource file using Template  
    $ robotx generate --resource=RES_NAME  

### Generate documates for the tests and resources of existing project
    $ robotx generate --doc=PRODUCT_PATH  


Debugger
--------
### Insert breakpoint to test case  
Insert keyword "debug" to test, then run test using pybot, 
and then test will be stoped at debug, and enter into shell debug mode.  
Example  

      *** Settings ***
      Library    robotx.lib.DebugLibrary.Debug

      ** Test Cases **
      Case 1234
          # keywords ...
          debug
          # keywords ...

### Debug test case in debug shell mode  
Type cmd to shell below  

    $ robotx debug  

Then you can type plain text format keywords.   
Note that if you want to use keywords coming from the third library,   
you need import the library firstly.  
And if you want do web page tests debug, you can directly type "web  url".  


Checker
-------
### Only check tests syntex
Type cmd to shell below  

    $ robotx check --cases=CASES_PATH  

### Check the format of tests name, tests tag, case id
Type cmd to shell below  

    $ robotx check --cases=CASES_PATH --tcms --planid=PLAN_ID  


Expander
--------
Refer to [seleniumext][seleniumext direct]

* Develop general test library
* Expand Selenium2library
* Expand native Selenium Webdriver



[Robot Framework]: http://robotframework.org/
[seleniumext direct]: https://github.com/idumpling/robotx/tree/master/robotx/lib/seleniumext
