#!/usr/bin/env python -O
"""
This is the test class for testing the Configuration module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.unit.TestConfiguration.py is part of The RTK Project
#
# All rights reserved.

import shutil
import sys
from os import environ, makedirs, name
from os.path import dirname, isfile
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import ConfigParser

from Configuration import RTKConf

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2016 Andrew "Weibullguy" Rowland'


class TestConfiguration(unittest.TestCase):
    """
    Class for testing the RTK Configuration.
    """

    def setUp(self):
        """
        (TestConfiguration) Method to setup the test fixture for the Configuration module.
        """

        self.siteDUT = RTKConf()

        self.userDUT = RTKConf('user')
        self.userDUT.conf_file = '/tmp/RTK/RTK.conf'
        self.userDUT.SITE_DIR = environ['HOME'] + '/.config/RTK'
        self.userDUT.conf_dir = '/tmp/RTK/'

        makedirs('/tmp/RTK/data')

    @attr(all=True, unit=True)
    def test00_initialize_site(self):
        """
        (TestConfiguration) __init__ should create an instance of the RTKConf object when initializing a site configuration
        """

        self.assertTrue(isinstance(self.siteDUT, RTKConf))

        if name == 'posix':
            self.assertEqual(self.siteDUT.OS, 'Linux')
            self.assertEqual(self.siteDUT.conf_dir,
                             environ['HOME'] + '/.config/RTK/')
            self.assertEqual(self.siteDUT.data_dir,
                             self.siteDUT.conf_dir + 'data/')
            self.assertEqual(self.siteDUT.icon_dir,
                             self.siteDUT.conf_dir + 'icons')
            self.assertEqual(self.siteDUT.log_dir,
                             self.siteDUT.conf_dir + 'logs/')
            self.assertEqual(self.siteDUT.conf_file,
                             self.siteDUT.conf_dir + 'site.conf')
            self.assertEqual(self.siteDUT.SITE_DIR, '/etc/RTK/')

    @attr(all=True, unit=True)
    def test01_initialize_user(self):
        """
        (TestConfiguration) __init__ should create an instance of the RTKConf object when initializing a user configuration
        """

        self.assertTrue(isinstance(self.userDUT, RTKConf))

        if name == 'posix':
            self.assertEqual(self.userDUT.OS, 'Linux')
            self.assertEqual(self.userDUT.conf_dir, '/tmp/RTK/')
            self.assertEqual(self.userDUT.data_dir,
                             environ['HOME'] + '/.config/RTK/data/')
            self.assertEqual(self.userDUT.icon_dir,
                             environ['HOME'] + '/.config/RTK/icons')
            self.assertEqual(self.userDUT.log_dir,
                             environ['HOME'] + '/.config/RTK/logs/')
            self.assertEqual(self.userDUT.prog_dir,
                             environ['HOME'] + '/analyses/rtk/')
            self.assertEqual(self.userDUT.conf_file,
                             self.userDUT.conf_dir + 'RTK.conf')
            self.assertEqual(self.userDUT.SITE_DIR,
                             environ['HOME'] + '/.config/RTK')

    @attr(all=True, unit=False)
    def test02_create_site_configuration(self):
        """
        (TestConfiguration) _create_site_configuration should return False on success
        """

        self.siteDUT.conf_file = '/tmp/site.conf'

        self.assertFalse(self.siteDUT._create_site_configuration())

    @attr(all=True, unit=True)
    def test03_create_user_configuration(self):
        """
        (TestConfiguration) _create_user_configuration should return False on success
        """

        self.assertFalse(self.userDUT._create_user_configuration())
        self.assertTrue(isfile('/tmp/RTK/RTK.conf'))
        self.assertTrue(isfile('/tmp/RTK/data/newprogram_mysql.sql'))
        self.assertTrue(isfile('/tmp/RTK/data/newprogram_sqlite3.sql'))
        self.assertTrue(isfile('/tmp/RTK/data/rtkcommon_mysql.sql'))
        self.assertTrue(isfile('/tmp/RTK/data/rtkcommon_sqlite3.sql'))

    def tearDown(self):
        """
        (TestConfiguration) Method to tear down the test fixture.
        """

        shutil.rmtree('/tmp/RTK')
