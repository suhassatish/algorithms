import json
import os
import unittest
from mml.parser import parse

PHASES = {
    'phase1': True,
    'phase2': False,
    'phase3': False
}

TEST_PATH = os.path.dirname(__file__)
DATASET_PATH = os.path.abspath(os.path.join(TEST_PATH, '../dataset'))


class Reader:
    def __init__(self, mml):
        self.mml = mml
        self.EOF = False

    def next_char(self):
        if self.EOF:
            raise ReadingException("Invalid reading after EOF")
        read = self.mml.read(1)
        if read == '':
            self.EOF = True
        return read

    def is_eof(self):
        return self.EOF


class ReadingException(ValueError):
    def __init__(self, message, *args):
        self.message = message
        super(ReadingException, self).__init__(message, *args)


class ParserTestCase(unittest.TestCase):
    """Test Case for MML Parser, based in an input text data and an expected result"""

    def __init__(self, mml, result, phase):
        self.mml = mml
        self.result = result
        self.phase = phase
        self.longMessage = True
        unittest.TestCase.__init__(self, methodName='run_test')

    def run_test(self):
        """Run a test to match parse results"""
        if not PHASES[self.phase]:
            self.skipTest('Phase %s is not enabled' % self.phase)
        with open(self.mml) as mml, open(self.result) as result:
            mml_file = os.path.split(self.mml)[1]
            mml_result = os.path.split(self.result)[1]
            expected_result = json.dumps(json.loads(result.read()))
            context = (self.phase, mml_file, mml_result)
            self.assertEqual(
                parse(Reader(mml)), expected_result,
                "In Phase %s, parsing of %s does not match %s" % context)


def phase_test_suite(phase_name):
    """Return all test suites for Phase 1"""
    phase_dir = os.path.join(DATASET_PATH, phase_name)
    phase_list = [(df, df.replace('.mml', '.result'))
                  for df in os.listdir(phase_dir) if df.endswith('.mml')]
    tests = []
    getpath = lambda file_name: os.path.join(phase_dir, file_name)
    for dataf, resultf in phase_list:
        tests.append(ParserTestCase(mml=getpath(dataf),
                                    result=getpath(resultf),
                                    phase=phase_name))
    return tests


def main():
    """Create and run test suite"""
    testsuite = unittest.TestSuite()
    testsuite.addTests(phase_test_suite('phase1'))
    testsuite.addTests(phase_test_suite('phase2'))
    testsuite.addTests(phase_test_suite('phase3'))
    unittest.TextTestRunner(verbosity=1).run(testsuite)


if __name__ == '__main__':
    main()
