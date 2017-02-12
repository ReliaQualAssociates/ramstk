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

        if name == 'posix':
            self.HOMEDIR = environ['HOME']
        elif name == 'nt':
            self.HOMEDIR = environ['USERPROFILE']

        self.siteDUT = RTKConf()
        self.siteDUT.SITE_DIR = '/home/andrew/.config/RTK'
        self.siteDUT.conf_dir = '/tmp/RTK'
        self.siteDUT.data_dir = self.siteDUT.conf_dir + '/data/'
        self.siteDUT.icon_dir = self.siteDUT.conf_dir + '/icons/'
        self.siteDUT.log_dir = self.siteDUT.conf_dir + '/logs/'
        self.siteDUT.conf_file = '/tmp/RTK/site.conf'

        self.userDUT = RTKConf('user')
        self.userDUT.SITE_DIR = '/home/andrew/.config/RTK'
        self.userDUT.conf_dir = '/tmp/RTK'
        self.userDUT.data_dir = self.userDUT.conf_dir + '/data/'
        self.userDUT.icon_dir = self.userDUT.conf_dir + '/icons/'
        self.userDUT.log_dir = self.userDUT.conf_dir + '/logs/'
        self.userDUT.conf_file = '/tmp/RTK/RTK.conf'

        try:
            makedirs('/tmp/RTK/data')
        except OSError:
            pass
        try:
            makedirs('/tmp/RTK/icons')
        except OSError:
            pass
        try:
            makedirs('/tmp/RTK/logs')
        except OSError:
            pass

    @attr(all=True, unit=True)
    def test00_initialize_site(self):
        """
        (TestConfiguration) __init__ should create an instance of the RTKConf object when initializing a site configuration
        """

        self.assertTrue(isinstance(self.siteDUT, RTKConf))

        if name == 'posix':
            self.assertEqual(self.siteDUT.OS, 'Linux')
            self.assertEqual(self.siteDUT.SITE_DIR, '/home/andrew/.config/RTK')
            self.assertEqual(self.siteDUT.conf_dir, '/tmp/RTK')
            self.assertEqual(self.siteDUT.data_dir,
                             self.siteDUT.conf_dir + '/data/')
            self.assertEqual(self.siteDUT.icon_dir,
                             self.siteDUT.conf_dir + '/icons/')
            self.assertEqual(self.siteDUT.log_dir,
                             self.siteDUT.conf_dir + '/logs/')
            self.assertEqual(self.siteDUT.conf_file,
                             self.siteDUT.conf_dir + '/site.conf')
            self.assertEqual(self.siteDUT.OS, 'Linux')

    @attr(all=True, unit=True)
    def test01_initialize_user(self):
        """
        (TestConfiguration) __init__ should create an instance of the RTKConf object when initializing a user configuration
        """

        self.assertTrue(isinstance(self.userDUT, RTKConf))

        if name == 'posix':
            self.assertEqual(self.userDUT.OS, 'Linux')
            self.assertEqual(self.userDUT.SITE_DIR, '/home/andrew/.config/RTK')
            self.assertEqual(self.userDUT.conf_dir, '/tmp/RTK')
            self.assertEqual(self.userDUT.data_dir,
                             self.userDUT.conf_dir + '/data/')
            self.assertEqual(self.userDUT.icon_dir,
                             self.userDUT.conf_dir + '/icons/')
            self.assertEqual(self.userDUT.log_dir,
                             self.userDUT.conf_dir + '/logs/')
            self.assertEqual(self.userDUT.prog_dir,
                             environ['HOME'] + '/analyses/rtk/')
            self.assertEqual(self.userDUT.conf_file,
                             self.userDUT.conf_dir + '/RTK.conf')

    @attr(all=True, unit=True)
    def test02_create_site_configuration(self):
        """
        (TestConfiguration) _create_site_configuration should return False on success
        """

        self.assertFalse(self.siteDUT._create_site_configuration())
        self.assertTrue(isfile('/tmp/RTK/site.conf'))

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

    @attr(all=True, unit=True)
    def test04_create_default_configuration_site(self):
        """
        (TestConfiguration) create_default_configuration should return False on success when creating site configuration
        """

        self.assertFalse(self.siteDUT.create_default_configuration())
        self.assertTrue(isfile('/tmp/RTK/site.conf'))

    @attr(all=True, unit=True)
    def test04a_create_default_configuration_user(self):
        """
        (TestConfiguration) create_default_configuration should return False on success when creating user configuration
        """

        self.assertFalse(self.userDUT.create_default_configuration())
        self.assertTrue(isfile('/tmp/RTK/RTK.conf'))
        self.assertTrue(isfile('/tmp/RTK/data/newprogram_mysql.sql'))
        self.assertTrue(isfile('/tmp/RTK/data/newprogram_sqlite3.sql'))
        self.assertTrue(isfile('/tmp/RTK/data/rtkcommon_mysql.sql'))
        self.assertTrue(isfile('/tmp/RTK/data/rtkcommon_sqlite3.sql'))

    @attr(all=True, unit=True)
    def test05_read_configuration(self):
        """
        (TestConfiguration) read_configuration should return False on success
        """

        _config = self.userDUT.read_configuration()
        self.assertTrue(isinstance(_config, ConfigParser.ConfigParser))

    @attr(all=True, unit=True)
    def test06_write_configuration(self):
        """
        (TestConfiguration) write_configuration should return False on success
        """

        self.userDUT.FRMULT = 1000000.0
        self.userDUT.RTK_MTIME = 100.0
        self.userDUT.PLACES = 6
        self.userDUT.RTK_MODE_SOURCE = 2
        self.userDUT.TABPOS = ['top', 'top', 'top']
        self.userDUT.BACKEND = 'mysql'
        self.userDUT.RTK_PROG_INFO = ['localhost', 3306, '', '', '']
        self.userDUT.RTK_FORMAT_FILE = ['', '', '', '', '', '', '', '', '', '',
                                        '', '', '', '', '', '', '', '']
        self.userDUT.RTK_COLORS = ['', '', '', '', '', '', '', '', '', '', '',
                                   '', '', '', '', '', '', '', '', '', '', '',
                                   '']

        self.assertFalse(self.userDUT.write_configuration())
