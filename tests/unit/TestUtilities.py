#!/usr/bin/env python -O
"""
This is the test class for testing the Utilities module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.unit.TestUtilities.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
from os.path import dirname, isfile

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from datetime import datetime
import logging

from Utilities import create_logger, split_string, none_to_string, \
                      string_to_boolean, date_to_ordinal, ordinal_to_date, \
                      dir_exists, file_exists, missing_to_default, \
                      error_handler

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestUtilities(unittest.TestCase):
    """
    Class for testing the RTK Utilities.
    """

    def setUp(self):
        """
        Setup the test fixture for the Utilities module.
        """

        pass

    @attr(all=True, unit=True)
    def test00_create_logger(self):
        """
        (TestUtilities) create_logger should return a logging.Logger instance
        """

        _log = create_logger("test.debug", logging.DEBUG, '/tmp/test.log')
        self.assertTrue(isinstance(_log, logging.Logger))
        self.assertTrue(isfile('/tmp/test.log'))

    @attr(all=True, unit=True)
    def test00a_create_logger_to_tty(self):
        """
        (TestUtilities) create_logger should return a logging.Logger instance
        """

        _log = create_logger("test.debug", logging.DEBUG, '', True)
        self.assertTrue(isinstance(_log, logging.Logger))
        self.assertTrue(isfile('/tmp/test.log'))

    @attr(all=True, unit=True)
    def test01_split_string(self):
        """
        (TestUtilities) split_string should return a list of strings split at the :
        """

        _strings = split_string('one:two:three')
        self.assertEqual(_strings[0], 'one')
        self.assertEqual(_strings[1], 'two')
        self.assertEqual(_strings[2], 'three')

    @attr(all=True, unit=True)
    def test02_none_to_string_None(self):
        """
        (TestUtilities) none_to_string should return an empty string when passed None
        """

        _string = none_to_string(None)
        self.assertEqual(_string, '')

    @attr(all=True, unit=True)
    def test02a_none_to_string_none(self):
        """
        (TestUtilities) none_to_string should return an empty string when passed 'None'
        """

        _string = none_to_string('None')
        self.assertEqual(_string, '')

    @attr(all=True, unit=True)
    def test02b_none_to_string_string(self):
        """
        (TestUtilities) none_to_string should return the original string when passed anything other than None or 'None'
        """

        _string = none_to_string('The original string')
        self.assertEqual(_string, 'The original string')

    @attr(all=True, unit=True)
    def test03_string_to_boolean_True(self):
        """
        (TestUtilities) string_to_boolean should return a 1 when passed True
        """

        _bool = string_to_boolean(True)
        self.assertEqual(_bool, 1)

    @attr(all=True, unit=True)
    def test03a_string_to_boolean_yes(self):
        """
        (TestUtilities) string_to_boolean should return a 1 when passed 'yes'
        """

        _bool = string_to_boolean('yes')
        self.assertEqual(_bool, 1)

    @attr(all=True, unit=True)
    def test03b_string_to_boolean_t(self):
        """
        (TestUtilities) string_to_boolean should return a 1 when passed 't'
        """

        _bool = string_to_boolean('t')
        self.assertEqual(_bool, 1)

    @attr(all=True, unit=True)
    def test03c_string_to_boolean_y(self):
        """
        (TestUtilities) string_to_boolean should return a 1 when passed 'y'
        """

        _bool = string_to_boolean('y')
        self.assertEqual(_bool, 1)

    @attr(all=True, unit=True)
    def test03d_string_to_boolean_False(self):
        """
        (TestUtilities) string_to_boolean should return a 0 when passed False
        """

        _bool = string_to_boolean(False)
        self.assertEqual(_bool, 0)

    @attr(all=True, unit=True)
    def test04_date_to_ordinal(self):
        """
        (TestUtilities) date_to_ordinal should return an integer when passed a date
        """

        _date = date_to_ordinal('2016-05-27')
        self.assertEqual(_date, 736111)

    @attr(all=True, unit=True)
    def test04a_date_to_ordinal_wrong_type(self):
        """
        (TestUtilities) date_to_ordinal should return the ordinal for 1970-01-01 when passed the wrong type
        """

        _date = date_to_ordinal(None)
        self.assertEqual(_date, 719163)

    @attr(all=True, unit=True)
    def test05_ordinal_to_date(self):
        """
        (TestUtilities) ordinal_to_date should return the date in YYYY-MM-DD format when passed an ordinal value
        """

        _date = ordinal_to_date(736111)
        self.assertEqual(_date, '2016-05-27')

    @attr(all=True, unit=True)
    def test05a_ordinal_to_date_value_error(self):
        """
        (TestUtilities) ordinal_to_date should return the current date in YYYY-MM-DD format when passed a non-ordinal value
        """

        _ordinal = datetime.now().toordinal()
        _today = str(datetime.fromordinal(int(_ordinal)).strftime('%Y-%m-%d'))

        _date = ordinal_to_date('Today')
        self.assertEqual(_date, _today)

    @attr(all=True, unit=True)
    def test06_dir_exists(self):
        """
        (TestUtilities) dir_exists should return True if the directory exists
        """

        self.assertTrue(dir_exists('/tmp'))

    @attr(all=True, unit=True)
    def test06a_dir_does_not_exist(self):
        """
        (TestUtilities) dir_exists should return False if the directory does not exists
        """

        self.assertFalse(dir_exists('/NotThere'))

    @attr(all=True, unit=True)
    def test07_file_exists(self):
        """
        (TestUtilities) file_exists should return True if the file exists
        """

        self.assertTrue(file_exists('/tmp/test.log'))

    @attr(all=True, unit=True)
    def test07a_file_does_not_exist(self):
        """
        (TestUtilities) file_exists should return False if the file does not exists
        """

        self.assertFalse(file_exists('/tmp/NotThere.txt'))

    @attr(all=True, unit=True)
    def test08_missing_to_default(self):
        """
        (TestUtilities) missing_to_default should return the default value if the original value is missing
        """

        _default = missing_to_default('', 10)
        self.assertEqual(_default, 10)

    @attr(all=True, unit=True)
    def test08a_missing_to_default_not_missing(self):
        """
        (TestUtilities) missing_to_default should return the original value if it is not missing
        """

        _default = missing_to_default(40, 10)
        self.assertEqual(_default, 40)

    @attr(all=True, unit=True)
    def test09_error_handler_type_error(self):
        """
        (TestUtilities) error_handler should return a 10 error code when passed a TypeError string
        """

        _error_code = error_handler(
                          ['The argument must be a string or a number dude!'])
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test09a_error_handler_value_error(self):
        """
        (TestUtilities) error_handler should return a 10 error code when passed a ValueError string
        """

        _error_code = error_handler(
                          ['That is invalid literal for int() with base 10'])
        self.assertEqual(_error_code, 10)

        _error_code = error_handler(
                          ['I could not convert string to float'])
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test09b_error_handler_zero_division_error(self):
        """
        (TestUtilities) error_handler should return a 20 error code when passed a ZeroDivisionError string
        """

        _error_code = error_handler(
                          ['float division by zero dunna work dude'])
        self.assertEqual(_error_code, 20)

        _error_code = error_handler(
                          ['That was integer division or modulo by zero'])
        self.assertEqual(_error_code, 20)

    @attr(all=True, unit=True)
    def test09c_error_handler_index_error(self):
        """
        (TestUtilities) error_handler should return a 40 error code when passed a IndexError string
        """

        _error_code = error_handler(
                          ['That index out of range'])
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test09d_error_handler_default(self):
        """
        (TestUtilities) error_handler should return a 1000 error code when passed a error string it can't parse
        """

        _error_code = error_handler(
                          ['Some kinda error message'])
        self.assertEqual(_error_code, 1000)
