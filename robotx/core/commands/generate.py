"""Sub command: generate

Usage: robotx generate [options]
"""

from robotx.core.base import BaseCommand
from robotx.core.exceptions import UsageError
from robotx.core.generator import generate_res
from robotx.core.generator import generate_docs
from robotx.core.generator import generate_suite
from robotx.core.generator import generate_project


class Command(BaseCommand):
    """Sub command 'generate' class."""

    def syntax(self):
        """Sub command 'generate' running format"""
        return "[-option]"

    def short_desc(self):
        """Sub command 'generate' short description"""
        return "Create new project, new test suite, new resource file"

    def long_desc(self):
        """Sub command 'generate' long description"""
        return "Easy to create a new project, new test suite, new resour."

    def add_options(self, parser):
        """Sub command 'generate' options"""
        parser.add_option('-p', '--project', dest="project_name",
                          metavar="PROJECT_NAME", help='Create new project.')
        parser.add_option('-s', '--suite', dest="suite_name",
                          metavar="SUITE_NAME",
                          help='Create new test suite file.')
        parser.add_option('-r', '--resource', dest="res_name",
                          metavar="RES_NAME",
                          help='Create new test resource file.')
        parser.add_option('-d', '--doc', dest="doc_project",
                          metavar="PRODUCT_PATH",
                          help='Create and update case, res and lib docs.')

    def run(self, args, opts):
        """Sub command 'generate' runner"""
        project = opts.project_name
        suite = opts.suite_name
        res = opts.res_name
        doc_project = opts.doc_project
        if (not project) and (not suite) and (not doc_project) and (not res):
            raise UsageError("One option must be specified!!!")
        # create project
        if project:
            generate_project(project)
        # create new suite file
        if suite:
            generate_suite(suite)
        # create new resource file
        if res:
            generate_res(res)
        # create docs
        if doc_project:
            print '\n', ' Doc Generating ... '.center(70, '*')
            generate_docs(doc_project)
            print '\n', ' DONE '.center(70, '*')
