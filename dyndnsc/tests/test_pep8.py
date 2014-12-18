# -*- coding: utf-8 -*-

import os
import unittest

import pep8

import dyndnsc


class Pep8ConformanceTestCase(unittest.TestCase):

    packages = [dyndnsc]

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_pep8_conformance(self):
        ignore_codes = (
            "E501",  # line length
        )
        pep8style = pep8.StyleGuide(show_source=True, ignore=ignore_codes)
        for package in self.packages:
            path = os.path.dirname(package.__file__)
            pep8style.input_dir(path)
        # assert we actually tested some files. Assume more than 50 files.
        self.assertTrue(50 < pep8style.options.report.counters['files'])
        self.assertEqual(0, pep8style.options.report.total_errors)
