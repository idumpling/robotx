Build & Config Jenkins Job for RobotX 
=====================================

The RobotX is a tool set for automation development with [Robot Framework][Robot Framework].


### Build new job  
For running tests with jenkins using RobotX, you need build a new "Build a free-style software project" job.  


### Add parameters below  
#### String Parameter: PROJECT_NAME  
**Required**    
The value is your project name, such as Beaker

#### String Parameter: TCMS_LOGIN_NAME  
**Required**    
The value is your user id for logging in Test Case Management System

#### Password Parameter: TCMS_LOGIN_PWD  
**Required**    
The value is your password for logging in Test Case Management System

#### String Parameter: TCMS_PLAN_ID  
**Required**    
The value is the plan id of your project

#### String Parameter: TCMS_RUN_ID  
**Optional**    
* If empty, RobotX will create new test run.  
* If giving, RobotX will not create new test run, just run all automated test cases in the giving run.  

#### Text Parameter: CASE_TAGS  
**Optional**    
* If empty, RobotX will not filter test case using any tag.  
* If giving, RobotX will filter test case using giving tags.  
* If giving more than one tag,  pls type one tag per line.  

#### Text Parameter: CASE_PRIORITIES  
**Optional**    
* If empty, RobotX will not filter test case using any priority.  
* If giving, RobotX will filter test case using giving priorities.  
* If giving more than one priorities, pls type one priority per line.  

#### Text Parameter: OTHER_VARIABLES  
**Optional**    
* If empty, RobotX will not change any variable when running tests.  
* If giving, RobotX will dynamically change the variables when running tests.
* If giving more than one tag,  pls type one tag per line.  
* The format of the value: UsualAccount:xgao.  
  Then RobotX will change the tests variable ${UsualAccount} to "xgao"  

### String Parameter: MASTER_IP  
**Required when run as distributted module**   
* If "--distributed" is given, the opts is required. i.e, 192.168.122.1

#### Text Parameter: SLAVE_IPS  
**Required when run as distributted module**   
* If "--distributed" is given, the opts is required. i.e, 192.168.122.1
* If giving more than one IP, pls type one priority per line.  
      for example:   
      root@192.168.122.56   
      root@192.168.122.153   

### String Parameter: SLAVE_PWD   
**Required when run as distributted module**   
**NOTE: all slaves can only have the same password(this's caused by one fabric bug.)**

### Restrict where this project can be run  
Type the label expression for selecting machine node.


### Source Code Management  
* Type your **Repository URL** to input box  
* Type the **Branch** of your project  
  Such as, origin/beaker  


### Execute shell  
#### Re-write tests info and result to TCMS(Test Case Management System)
Type cmd to Jenkins "Execute Shell" below
  
    $ robotx run --jenkins --tcms

#### Do not re-write anything to TCMS  
Type cmd to Jenkins "Execute Shell" below  

    $ robotx run --jenkins

### Parallel run tests on more than one PC   

    $ robotx run --jenkins --tcms --distributed
    or   
    $ robotx run --jenkins --distributed
   

### Post-build Actions  
* Directory of Robot output: $WORKSPACE/tests/$PROJECT_NAME/results
* Log/Report link: report.html
* Output xml name: output.xml
* Report html name: report.html
* Log html name: log.html


