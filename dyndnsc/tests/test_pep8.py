# -*- coding: utf-8 -*-

import os
import unittest

import pep8

import dyndnsc

MAX_LINE_LENGTH = 132

# sequence of "Ennn" strings to ignore:
IGNORE_CODES = ()


class Pep8ConformanceTestCase(unittest.TestCase):

    packages = [dyndnsc]

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_pep8_conformance(self):
        pep8style = pep8.StyleGuide(show_source=True, ignore=IGNORE_CODES,
                                    max_line_length=MAX_LINE_LENGTH)
        for package in self.packages:
            path = os.path.dirname(package.__file__)
            pep8style.input_dir(path)
        # assert we actually tested some files. Assume more than 50 files.
        self.assertTrue(50 < pep8style.options.report.counters['files'])
        self.assertEqual(0, pep8style.options.report.total_errors)
