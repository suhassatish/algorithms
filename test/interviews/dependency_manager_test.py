import unittest
import sys
import os
from contextlib import contextmanager
from StringIO import StringIO
from app.interviews.dependency_manager import DependencyManager, DependencyManagerClient


class MyTest(unittest.TestCase):
    """
    python -m unittest test.interviews.dependency_manager_test.MyTest.integration_test
    """
    def integration_test(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data',
                                 'dependency_manager_data', 'sample_input.txt')
        dmc = DependencyManagerClient()
        with captured_output() as (out, err):
            dmc.parse_file(test_file)

        actual_output = out.getvalue()

        expected_output_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data',
                                 'dependency_manager_data', 'sample_output.txt')
        with open(expected_output_file, 'r') as f:
            expected_contents = f.read()
            assert(expected_contents == actual_output)

    def test_circular_dependency(self):
        test_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data',
                                 'dependency_manager_data', 'sample_input_circular_dep.txt')
        dmc = DependencyManagerClient()
        with captured_output() as (out, err):
            dmc.parse_file(test_file)
        actual_output = out.getvalue()
        expected_output_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data',
                                 'dependency_manager_data', 'sample_output_circular_dep.txt')
        with open(expected_output_file, 'r') as f:
            expected_contents = f.read()
            assert(expected_contents == actual_output)


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err