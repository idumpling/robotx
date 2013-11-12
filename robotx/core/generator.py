"""RobotX Generator handler"""

import os
import re
import sys
import shutil
from os.path import join
from os.path import exists

from robot.libdoc import LibDoc
from robot.testdoc import TestDoc

import robotx
from robotx.utils import copy


TEMPLATES_PATH = join(robotx.__path__[0], 'template', 'project_template')
RES_TEMPLATE = join(TEMPLATES_PATH, 'resources', 'home_page.txt')
SUITE_TEMPLATE = join(TEMPLATES_PATH,
                      'cases', '01__webui', '01__wiki_test.txt')


class MyLibDoc(LibDoc):

    def _exit(self, rc):
        """By default _exit is run for exiting system.
        Disable it."""
        pass


class MyTestDoc(TestDoc):

    def _exit(self, rc):
        """By default _exit is run for exiting system.
        Disable it."""
        pass


def generate_project(project):
    """for generating a format project"""
    directory = os.getcwd()
    template_dir = TEMPLATES_PATH
    # error if
    if not re.search(r'^[A-Z]\w*$', project):
        print 'Error: Project names must begin with a capital letter. \
              \nand contain only letters, numbers and underscores.'
        sys.exit(1)
    elif exists(project):
        print "Error: project %r already exists" % project
        sys.exit(1)
    copy.copy_helper(project, directory, template_dir)


def generate_suite(suite):
    """for generating a format Robot Framework test suite file"""
    directory = os.getcwd()
    suite_template = SUITE_TEMPLATE
    new_suite_path = join(directory, suite)
    # error if
    if not re.search(r'^[\w]\w*.txt$', suite):
        print 'Error: suite name must begin with letter or number. \
              \nand must end with .txt \
              \nand contain only letters, numbers and underscores.'
        sys.exit(1)
    elif exists(suite):
        print "Error: suite %r already exists" % suite
        sys.exit(1)
    shutil.copy(suite_template, new_suite_path)


def generate_res(res):
    """for generating a format Robot Framework resource file"""
    directory = os.getcwd()
    res_template = RES_TEMPLATE
    new_res_path = join(directory, res)
    # error if
    if not re.search(r'^[\w]\w*.txt$', res):
        print 'Error: res name must begin with letter or number. \
              \nand must end with .txt \
              \nand contain only letters, numbers and underscores.'
        sys.exit(1)
    elif exists(res):
        print "Error: resource %r already exists" % res
        sys.exit(1)
    shutil.copy(res_template, new_res_path)


def generate_docs(doc_project):
    """for generating all cases doc and resources doc"""
    if doc_project.endswith('/'):
        doc_project = doc_project[:-1]
    doc_project = doc_project.capitalize()
    project_path = join(os.path.curdir, doc_project)
    case_path = join(project_path, 'cases')
    res_path = join(project_path, 'resources')
    doc_path = join(project_path, 'doc')
    # delete all old docs
    delete_file_folder(doc_path)
    # test case document
    print 'Generate %s automated test cases doc ...' % doc_project
    case_doc_name = '%s_cases_doc.html' % doc_project.lower()
    the_case_doc = join(doc_path, case_doc_name)
    MyTestDoc().execute_cli(['--title', '%s Automated Cases Document'
                            % doc_project,
                            '--name', 'All automated cases document',
                            case_path, the_case_doc])
    # resources and libs document
    print '\nGenerate %s resources, libs docs ...' % doc_project
    # get all resources files
    res_files = walk_dir(res_path)
    res_doc_dir = join(doc_path, 'resource_docs')
    if not os.path.exists(res_doc_dir):
        os.makedirs(res_doc_dir)
    for res in res_files:
        if res.find('.py') >= 0:
            # temporarily igore lib files
            continue
        the_res_path = join(res_path, res)
        res_doc_name = res.split('.')[0] + '.html'
        the_res_doc = join(res_doc_dir, res_doc_name)
        MyLibDoc().execute_cli([the_res_path, the_res_doc])


def walk_dir(dir, topdown=True):
    """getting all files under dirs"""
    all_files = []
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            all_files.append(os.path.join(name))
    return all_files


def delete_file_folder(src):
    """delete files and folders"""
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_folder(itemsrc)
