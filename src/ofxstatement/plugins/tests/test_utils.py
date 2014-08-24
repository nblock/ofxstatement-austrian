#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import datetime
import os
import unittest

from ofxstatement.plugins.utils import clean_multiple_whitespaces, fix_amount_string

class TestCleanMultipleWhiteSpaces(unittest.TestCase):
    """Unit tests for clean_multiple_whitespaces helper."""
    expected = "This is a test"

    def test_just_spaces(self):
        self.assertEqual(clean_multiple_whitespaces("This    is  a test"),
               self.expected)

    def test_just_tabs(self):
        self.assertEqual(clean_multiple_whitespaces("This	is	a	test"),
               self.expected)

    def test_mixed_tabs_and_spaces(self):
        self.assertEqual(clean_multiple_whitespaces(" This	is  a test  "),
               self.expected)

    def test_empty_string(self):
        self.assertEqual(clean_multiple_whitespaces(""), "")

    def test_string_with_spaces(self):
        self.assertEqual(clean_multiple_whitespaces("       "), "")


class TestFixAmountString(unittest.TestCase):
    """Unit tests for fix_amount_string helper."""

    def test_integer_string(self):
        self.assertEqual(fix_amount_string("11"), "11")

    def test_no_thousand_mark(self):
        self.assertEqual(fix_amount_string("1,23"), "1.23")

    def test_with_thousand_mark(self):
        self.assertEqual(fix_amount_string("100.234,23"), "100234.23")

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
