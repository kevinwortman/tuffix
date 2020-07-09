"""
Unit tests for Tuffix utility
AUTHOR: Kevin Wortman
"""

import io, pathlib, unittest

import packaging.version, pyfakefs

from tuffixlib import *

class TestGlobals(unittest.TestCase):
    def test_VERSION(self):
        self.assertTrue(isinstance(VERSION, packaging.version.Version))

    def test_STATE_PATH(self):
        self.assertTrue(isinstance(STATE_PATH, pathlib.Path))
        self.assertEqual('.json', STATE_PATH.suffix)

    def test_DEFAULT_BUILD_CONFIG(self):
        self.assertTrue(isinstance(DEFAULT_BUILD_CONFIG, BuildConfig))
        self.assertEqual(VERSION, DEFAULT_BUILD_CONFIG.version)
        self.assertEqual(STATE_PATH, DEFAULT_BUILD_CONFIG.state_path)

class TestExceptionClasses(unittest.TestCase):
    MESSAGE = 'description of the problem that occurred'

    def test_MessageException(self):
        with self.assertRaises(ValueError):
            MessageException(None)
        e = MessageException(self.MESSAGE)
        self.assertEqual(self.MESSAGE, e.message)

    def test_UsageError(self):
        with self.assertRaises(ValueError):
            UsageError(None)
        e = UsageError(self.MESSAGE)
        self.assertTrue(isinstance(e, MessageException))
        self.assertEqual(self.MESSAGE, e.message)

    def test_UsageError(self):
        with self.assertRaises(ValueError):
            UsageError(None)
        e = UsageError(self.MESSAGE)
        self.assertTrue(isinstance(e, MessageException))
        self.assertEqual(self.MESSAGE, e.message)

    def test_EnvironmentError(self):
        with self.assertRaises(ValueError):
            EnvironmentError(None)
        e = EnvironmentError(self.MESSAGE)
        self.assertTrue(isinstance(e, MessageException))
        self.assertEqual(self.MESSAGE, e.message)

    def test_StatusError(self):
        with self.assertRaises(ValueError):
            StatusError(None)
        e = StatusError(self.MESSAGE)
        self.assertTrue(isinstance(e, MessageException))
        self.assertEqual(self.MESSAGE, e.message)

    def test_StatusWarning(self):
        with self.assertRaises(ValueError):
            StatusWarning(None)
        e = StatusWarning(self.MESSAGE)
        self.assertTrue(isinstance(e, MessageException))
        self.assertEqual(self.MESSAGE, e.message)

class TestBuildConfig(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(ValueError):
            BuildConfig(None, STATE_PATH)
        with self.assertRaises(ValueError):
            BuildConfig(VERSION, None)
        version = packaging.version.Version('1.2.3')
        state_path = pathlib.Path('state.json')
        obj = BuildConfig(version, state_path)
        self.assertEqual(version, obj.version)
        self.assertEqual(state_path, obj.state_path)

class TestState(unittest.TestCase):
    build_config = DEFAULT_BUILD_CONFIG
    version = packaging.version.Version('1.2.3')
    installed = ['base', '131']

    def test_constructor(self):

        with self.assertRaises(ValueError):
            State(None, self.version, self.installed)
        with self.assertRaises(ValueError):
            State(self.build_config, None, self.installed)
        with self.assertRaises(ValueError):
            State(self.build_config, self.version, None)
        with self.assertRaises(ValueError):
            State(self.build_config, self.version, [1, 2, 3])
        obj = State(self.build_config, self.version, self.installed)
        self.assertEqual(self.version, obj.version)
        self.assertEqual(self.installed, obj.installed)

    def test_write(self):
        obj = State(self.build_config, self.version, self.installed)

        # TODO: check that writing to a pyfakefs works

if __name__ == '__main__':
    unittest.main()
