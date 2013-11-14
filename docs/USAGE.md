RobotX Usage
============

The RobotX is a tool set for automation development with [Robot Framework][Robot Framework].

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
Insert keyword "debug" to test, then run test using pybot, and then test will be stoped at debug, and enter into shell debug mode.  
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