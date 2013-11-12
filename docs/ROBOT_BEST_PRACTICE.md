Robot Framework Best Practices
==============================


Introduction
------------
A guide to developing and running automation with [Robot Framework][Robot Framework].

If you are looking to make the jump from beginner to pro, or just trying to sharpen your skills, you'll find Robot Framework Best Practices chock full of knowledge ...  

... Okay, I admit that this is just a draft doc writing by myself by now. it still need to be improved continuously by you.

So, If you see a problem, or disagree with something, Please don't hesitation to contact me via emial or file an issue.

I'd love to hear your feedback, and I believe that it will become worthy of it's name soon later.


Tests and Resources Lay-out
---------------------------
* Tabs or Spaces?  
Spaces are the preferred indentation method.  
If use tab, you'd better set your editor as "Convert Indentation Spaces".  

* Maximum Line Length  
Since Robot Framework is a Domain Specific Language, and sometime the sentance may a little long, we don't need limit the maximum line length.

But we should try to keep the test name and keyword concise.
Once the name or keyword is a little long, you'd better use "..." as Line break. Example is as follows,  

    Open StartProcess SimpleDemoProcess Page
        [Documentation]    Open Simple demo process page 
        ...                for creating a new Simple demo process
        ${result status} =                  Run Keyword And Return Status
                       ...                  Verify Sub-menu Show Up
        Run Keyword If                      ${result status}
                       ...                  Click Element
                       ...                  ${MENU-SIMPLE-DEMO-PROCESS LOCATOR}
        Verify SimpleDemo Page Is Opened


* Blank Lines
Separate tables with two blank lines.  
Separate tests and keywords with a single blank line.

* Documatations
Better add documentation for every suite, test, keyword and library.  
For writing good documentation strings, refer to [Robot Framework Documente String][Robot Doc].


Whitespace in Expressions
-------------------------
Use at least 4 spaces between columns, If use non HTML format as your tests and resources file.


Naming Conventions
------------------
* Suite Names: use the "lower_case_with_underscores".  
* Test Steps: use the "Given/When/Then".  
* Keyword Names: use the "Cap Words" style.  
* Global General Variable Names: use the "${CapWords}".  
* Page Elements Variable Names: use the "${CapWords Locator}".  
  **NOTE:** the "Locator" includes "Locator", "ID", "Name", "Text", "Class", etc.


Robot Framework Projects
------------------------
    * Test and Resource Format
      We use Plain Text format. Example is as follows,

    *** Settings ***
    Documentation    A test suite with a single test for try page objects
    ...
    ...              against the Wikipedia Site
    Resource         ../../resources/common_res.txt
    Test Teardown    Close All Browsers


    *** Test Cases ***
    Case 317459 demo show 1
        [Documentation]    This Test Case uses a higher level wikipedia resource
        ...                for showing Page Resource.
        [Tags]             ID_317459    tag1
        Given open browser to wiki home page
        When search for robot framework on wikipedia
        Then from Robot framework wiki page goto RIDE page

    Case 317460 demo show 2
        [Documentation]    This Test Case uses a higher level wikipedia resource
        ...                for showing Page Resource.
        [Tags]             ID_317460    tag2
        Then search a string


    *** Settings ***
    Documentation     A resource file containing WiKi home page specific keywords.
    ...
    ...               domain specific language. They utilize keywords provided
    ...               by the imported Selenium2Library.
    Library           Selenium2Library
    Resource          common_res.txt


    *** Variables ***
    #************************** Common Variables ******************************
    ${HomePage URL}              http://${Server}
    ${HomePage Title}            Wikipedia
    ${Search Text}               Robot Framework

    #************************** Page Elements *********************************
    ${SearchInput ID}            searchInput
    ${SearchSubmitButton ID}     go


    *** Keywords ***
    Open Browser To Wiki Home Page
        [Documentation]       For Open WiKi Home Page.
        Open Browser          ${HomePage URL}             ${Browser}
        Maximize Browser Window
        Set Selenium Speed    ${Delay}
        Title Should Be       ${HomePage Title}

    Search For Robot Framework
        [Documentation]       do search operation
        Input Text            ${SearchInput ID}           ${Search Text}
        Click Button          ${SearchSubmitButton ID}


* project directory structure  
Assume the project name is "Demo"  

        .
        |-- Demo
        |   |-- cases
        |   |   |-- 01__webui
        |   |   |   `-- 01__wiki_test.txt
        |   |   |-- 02__cmd
        |   |   |   |-- 01__gherkin.txt
        |   |   |   |-- ...
        |   |   `-- ...
        |   |-- doc
        |   |   |-- demo_cases_doc.html
        |   |   `-- resource_docs
        |   |       |-- cmd_res.html
        |   |       |-- common_res.html
        |   |       |-- ...
        |   |-- others
        |   |   `-- ...
        |   |-- resources
        |   |   |-- CalculatorLibrary.py
        |   |   |-- cmd_res.txt
        |   |   |-- common_res.txt
        |   |   |-- home_page.txt
        |   |   |-- ride_page.txt
        |   |   |-- search_page.txt
        |   |   `-- wiki_robot_page.txt
        |   |-- results
        |   |   `-- ...
        |   `-- scripts
        |       `-- ...



* Page Resources with UI Mapping in web automation  
As we know, in web system automation developing, for reducing the amount of duplicated code and means that if the UI changes, the fix need only be applied in one place, we commonly use [Page Objects][Page Objects] with [UI Mapping][UI Mapping].  

But Robot Framework (or simply RF) is a not an Object Oriented Framework.  So in the spirit of Page Objects and RF, we should call it Page Resources.  

Use Page Resources for structure scalable and maintainable acceptance test suite. Following picture illustrates the architecture of automation project with Page Resources.

![Architecture][Page Res Arch]


About UI Mapping, it can be easily implemented by Variables table in Robot Framework.  
For example,  


    *** Variables ***
    #************************ Common Variables ****************************
    ${HOME PAGE TITLE}                  Maitai - Business Process Engine
    
    #************************* Page Elements ******************************
    ${LOGO LOCATOR}                     css = a.logo strong
    #******MENU
    ${MENU-MY-TASKS LOCATOR}            css = a[href="#task"]
    ${MENU-PROCESSES LOCATOR}           css = a[href="#process/instance"]
    ${MENU-ADMIN LOCATOR}               css = a[href="#process/definitions"]
    ${MENU-START-PROCESS LOCATOR}       css = a[href="#process"]


References
----------
* [Robot Framework Guide][Robot Guide]
* [Python PEP8][Python PEP8]


Copyright
---------
This document has been placed in the public domain.


[Robot Framework]: http://robotframework.org/
[Python PEP8]: http://www.python.org/dev/peps/pep-0008/
[Robot Guide]: http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html  
[Page Objects]: https://code.google.com/p/selenium/wiki/PageObjects
[UI Mapping]: http://www.seleniumhq.org/docs/06_test_design_considerations.jsp#ui-mapping
[Robot Doc]: http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html#documentation-formatting
[Page Res Arch]: https://github.com/fdumpling/temp/raw/master/docs/page_res_arch.png

