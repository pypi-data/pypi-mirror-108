import os
import json

from unittest import TestCase
from arm64_tester import Test


class TestTest(TestCase):

    def test_file(self):
        os.chdir('./test')

        submission_file = os.path.abspath(os.path.join(
            os.path.curdir, 'resources', 'week3', 'sol_opmat.zip'))
        subroutine_file = os.path.abspath(os.path.join(
            os.path.curdir, 'resources', 'week3', 'subroutines.yaml'))
        tests_file = os.path.abspath(os.path.join(
            os.path.curdir, 'resources', 'week3', 'tests.yaml'))

        test_suite = Test(submission_file, subroutine_file, tests_file)

        print(json.dumps(test_suite.run(), indent=4))
