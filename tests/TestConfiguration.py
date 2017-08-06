#!/usr/bin/env python -O
"""
This is the test class for testing the Configuration module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.unit.TestConfiguration.py is part of The RTK Project
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

import shutil
import sys
from os import environ, makedirs, name
from os.path import dirname, isfile
sys.path.insert(0, dirname(dirname(__file__)) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from Configuration import Configuration

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

        self.DUT = Configuration()

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
    def test00_initialize_configuration(self):
        """
        (TestConfiguration) __init__ should create an instance of the Configuration object when initializing
        """

        self.assertTrue(isinstance(self.DUT, Configuration))

        self.assertEqual(self.DUT.RTK_MODE, '')
        self.assertEqual(self.DUT.RTK_SITE_CONF, '')
        self.assertEqual(self.DUT.RTK_PROG_CONF, '')
        self.assertEqual(self.DUT.RTK_DEBUG_LOG, '')
        self.assertEqual(self.DUT.RTK_IMPORT_LOG, '')
        self.assertEqual(self.DUT.RTK_USER_LOG, '')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE, {})
        self.assertEqual(self.DUT.RTK_COLORS, {})
        self.assertEqual(self.DUT.RTK_PREFIX, {})
        self.assertEqual(self.DUT.RTK_ACTION_CATEGORY, {})
        self.assertEqual(self.DUT.RTK_INCIDENT_CATEGORY, {})
        self.assertEqual(self.DUT.RTK_SEVERITY, {})
        self.assertEqual(self.DUT.RTK_ACTIVE_ENVIRONMENTS, {})
        self.assertEqual(self.DUT.RTK_DORMANT_ENVIRONMENTS, {})
        self.assertEqual(self.DUT.RTK_SW_DEV_ENVIRONMENTS, {})
        self.assertEqual(self.DUT.RTK_AFFINITY_GROUPS, {})
        self.assertEqual(self.DUT.RTK_WORKGROUPS, {})
        self.assertEqual(self.DUT.RTK_FAILURE_PROBABILITY, {})
        self.assertEqual(self.DUT.RTK_SW_LEVELS, {})
        self.assertEqual(self.DUT.RTK_DETECTION_METHODS, {})
        self.assertEqual(self.DUT.RTK_SW_TEST_METHODS, {})
        self.assertEqual(self.DUT.RTK_ALLOCATION_MODELS, {})
        self.assertEqual(self.DUT.RTK_DAMAGE_MODELS, {})
        self.assertEqual(self.DUT.RTK_HR_MODEL, {})
        self.assertEqual(self.DUT.RTK_LIFECYCLE, {})
        self.assertEqual(self.DUT.RTK_SW_DEV_PHASES, {})
        self.assertEqual(self.DUT.RTK_RPN_DETECTION, {})
        self.assertEqual(self.DUT.RTK_RPN_SEVERITY, {})
        self.assertEqual(self.DUT.RTK_RPN_OCCURRENCE, {})
        self.assertEqual(self.DUT.RTK_ACTION_STATUS, {})
        self.assertEqual(self.DUT.RTK_INCIDENT_STATUS, {})
        self.assertEqual(self.DUT.RTK_CONTROL_TYPES, [])
        self.assertEqual(self.DUT.RTK_COST_TYPE, {})
        self.assertEqual(self.DUT.RTK_HR_TYPE, {})
        self.assertEqual(self.DUT.RTK_INCIDENT_TYPE, {})
        self.assertEqual(self.DUT.RTK_MTTR_TYPE, {})
        self.assertEqual(self.DUT.RTK_REQUIREMENT_TYPE, {})
        self.assertEqual(self.DUT.RTK_VALIDATION_TYPE, {})
        self.assertEqual(self.DUT.RTK_SW_APPLICATION, {})
        self.assertEqual(self.DUT.RTK_CATEGORIES, {})
        self.assertEqual(self.DUT.RTK_CRITICALITY, {})
        self.assertEqual(self.DUT.RTK_FAILURE_MODES, {})
        self.assertEqual(self.DUT.RTK_HAZARDS, {})
        self.assertEqual(self.DUT.RTK_MANUFACTURERS, {})
        self.assertEqual(self.DUT.RTK_MEASUREMENT_UNITS, {})
        self.assertEqual(self.DUT.RTK_OPERATING_PARAMETERS, {})
        self.assertEqual(self.DUT.RTK_S_DIST, {})
        self.assertEqual(self.DUT.RTK_STAKEHOLDERS, {})
        self.assertEqual(self.DUT.RTK_SUBCATEGORIES, {})
        self.assertEqual(self.DUT.RTK_USERS, {})
        self.assertEqual(self.DUT.RTK_RISK_POINTS, [4, 10])
        self.assertEqual(self.DUT.RTK_MODE_SOURCE, 1)
        self.assertEqual(self.DUT.RTK_FMECA_METHOD, 1)
        self.assertEqual(self.DUT.RTK_RPN_FORMAT, 0)
        self.assertEqual(self.DUT.RTK_COM_BACKEND, '')
        self.assertEqual(self.DUT.RTK_BACKEND, '')
        self.assertEqual(self.DUT.RTK_COM_INFO, {})
        self.assertEqual(self.DUT.RTK_PROG_INFO, {})
        self.assertEqual(self.DUT.RTK_MODULES, {})
        self.assertEqual(self.DUT.RTK_PAGE_NUMBER, {})
        self.assertEqual(self.DUT.RTK_HR_MULTIPLIER, 1000000.0)
        self.assertEqual(self.DUT.RTK_DEC_PLACES, 6)
        self.assertEqual(self.DUT.RTK_MTIME, 10.0)
        self.assertEqual(self.DUT.RTK_TABPOS,
                         {'listbook': 'top', 'modulebook': 'bottom',
                          'workbook': 'bottom'})
        self.assertEqual(self.DUT.RTK_GUI_LAYOUT, 'advanced')
        self.assertEqual(self.DUT.RTK_METHOD, 'STANDARD')

        if name == 'posix':
            self.assertEqual(self.DUT.RTK_OS, 'Linux')
            self.assertEqual(self.DUT.RTK_LOCALE, 'en_US')
            self.assertEqual(self.DUT.RTK_SITE_DIR, '/etc/RTK')
            self.assertEqual(self.DUT.RTK_HOME_DIR, environ['HOME'])
            self.assertEqual(self.DUT.RTK_DATA_DIR, '/usr/share/RTK')
            self.assertEqual(self.DUT.RTK_ICON_DIR, '/usr/share/pixmaps/RTK')
            self.assertEqual(self.DUT.RTK_LOG_DIR, '/var/log/RTK')
            self.assertEqual(self.DUT.RTK_PROG_DIR,
                             self.DUT.RTK_HOME_DIR + '/analyses/rtk')
            self.assertEqual(self.DUT.RTK_CONF_DIR, '')

    @attr(all=True, unit=True)
    def test01a_set_site_variables(self):
        """
        (TestConfiguration) set_site_variables should return False on success
        """

        self.assertFalse(self.DUT.set_site_variables())

        if name == 'posix':
            self.assertEqual(self.DUT.RTK_SITE_DIR,
                             '/etc/RTK')
            self.assertEqual(self.DUT.RTK_HOME_DIR, environ['HOME'])
            self.assertEqual(self.DUT.RTK_CONF_DIR,
                             self.DUT.RTK_HOME_DIR + '/.config/RTK')
            self.assertEqual(self.DUT.RTK_DATA_DIR,
                             self.DUT.RTK_HOME_DIR + '/.config/RTK/data')
            self.assertEqual(self.DUT.RTK_ICON_DIR,
                             self.DUT.RTK_HOME_DIR + '/.config/RTK/icons')
            self.assertEqual(self.DUT.RTK_LOG_DIR,
                             self.DUT.RTK_HOME_DIR + '/.config/RTK/logs')
            self.assertEqual(self.DUT.RTK_PROG_DIR,
                             self.DUT.RTK_HOME_DIR + '/analyses/rtk')
            self.assertEqual(self.DUT.RTK_SITE_CONF,
                             self.DUT.RTK_CONF_DIR + '/site.conf')

    @attr(all=True, unit=True)
    def test02a_set_user_variables(self):
        """
        (TestConfiguration) set_user_variables should return False on success
        """

        self.assertFalse(self.DUT.set_user_variables())

        self.assertEqual(self.DUT.RTK_PROG_CONF,
                         self.DUT.RTK_CONF_DIR + '/RTK.conf')

    @attr(all=True, unit=True)
    def test03a_create_site_configuration(self):
        """
        (TestConfiguration) _create_site_configuration should return False on success
        """

        self.DUT.RTK_SITE_DIR = '/tmp/RTK'
        self.DUT.RTK_HOME_DIR = '/tmp/RTK'
        self.DUT.RTK_SITE_CONF = self.DUT.RTK_SITE_DIR + '/site.conf'

        self.assertFalse(self.DUT._create_site_configuration())
        self.assertTrue(isfile('/tmp/RTK/site.conf'))

    @attr(all=True, unit=True)
    def test04a_create_user_configuration(self):
        """
        (TestConfiguration) create_user_configuration should return False on success
        """

        self.DUT.RTK_SITE_DIR = dirname(dirname(__file__)) + '/config'
        self.DUT.RTK_HOME_DIR = '/tmp/RTK'
        self.DUT.set_site_variables()
        self.DUT.set_user_variables()

        self.assertFalse(self.DUT.create_user_configuration())
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/RTK.conf'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/alt_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/dataset_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/ffmeca_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/fmeca_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/fraca_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/function_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/hardware_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/incident_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR +
                               '/mechanisms_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/modes_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/part_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR +
                               '/requirement_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/revision_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR +
                               '/rgincident_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/risk_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/sfmeca_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/sia_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/software_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR +
                               '/stakeholder_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR + '/testing_format.xml'))
        self.assertTrue(isfile(self.DUT.RTK_CONF_DIR +
                               '/validation_format.xml'))

    @attr(all=True, unit=True)
    def test05a_read_site_configuration(self):
        """
        (TestConfiguration) _read_site_configuration should return False on success
        """

        self.DUT.RTK_SITE_DIR = dirname(dirname(__file__)) + '/config'
        self.DUT.RTK_HOME_DIR = '/tmp/RTK'
        self.DUT.set_site_variables()
        self.DUT.set_user_variables()
        self.DUT.create_user_configuration()

        self.assertFalse(self.DUT._read_site_configuration())

        self.assertEqual(self.DUT.RTK_COM_BACKEND, 'sqlite')
        self.assertEqual(self.DUT.RTK_COM_INFO['host'], 'localhost')
        self.assertEqual(self.DUT.RTK_COM_INFO['socket'], '3306')
        self.assertEqual(self.DUT.RTK_COM_INFO['database'], '')
        self.assertEqual(self.DUT.RTK_COM_INFO['user'], 'user')
        self.assertEqual(self.DUT.RTK_COM_INFO['password'], 'password')

    @attr(all=True, unit=True)
    def test05b_read_configuration(self):
        """
        (TestConfiguration) read_configuration should return False on success
        """

        self.DUT.RTK_SITE_DIR = dirname(dirname(__file__)) + '/config'
        self.DUT.RTK_HOME_DIR = '/tmp/RTK'
        self.DUT.set_site_variables()
        self.DUT.set_user_variables()
        self.DUT.create_user_configuration()

        self.assertFalse(self.DUT.read_configuration())
        self.assertEqual(self.DUT.RTK_COLORS['revisionfg'], '#000000')
        self.assertEqual(self.DUT.RTK_COLORS['functionfg'], '#0000FF')
        self.assertEqual(self.DUT.RTK_COLORS['requirementfg'], '#000000')
        self.assertEqual(self.DUT.RTK_COLORS['assemblyfg'], '#000000')
        self.assertEqual(self.DUT.RTK_COLORS['partfg'], '#000000')
        self.assertEqual(self.DUT.RTK_COLORS['overstressfg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['taggedfg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['nofrmodelfg'], '#A52A2A')
        self.assertEqual(self.DUT.RTK_COLORS['softwarefg'], '#000000')
        self.assertEqual(self.DUT.RTK_COLORS['incidentfg'], '#000000')
        self.assertEqual(self.DUT.RTK_COLORS['validationfg'], '#00FF00')
        self.assertEqual(self.DUT.RTK_COLORS['testfg'], '#000000')
        self.assertEqual(self.DUT.RTK_COLORS['survivalfg'], '#000000')
        self.assertEqual(self.DUT.RTK_COLORS['revisionbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['functionbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['requirementbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['assemblybg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['partbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['overstressbg'], '#FF0000')
        self.assertEqual(self.DUT.RTK_COLORS['taggedbg'], '#00FF00')
        self.assertEqual(self.DUT.RTK_COLORS['softwarebg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['incidentbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['validationbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['testbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RTK_COLORS['survivalbg'], '#FFFFFF')

        self.assertEqual(self.DUT.RTK_FORMAT_FILE['revision'],
                         'revision_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['function'],
                         'function_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['requirement'],
                         'requirement_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['hardware'],
                         'hardware_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['software'],
                         'software_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['incident'],
                         'incident_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['validation'],
                         'validation_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['testing'],
                         'testing_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['part'], 'part_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['sia'], 'sia_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['fmeca'], 'fmeca_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['rgincident'],
                         'rgincident_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['stakeholder'],
                         'stakeholder_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['dataset'],
                         'dataset_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['risk'], 'risk_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['ffmeca'],
                         'ffmeca_format.xml')
        self.assertEqual(self.DUT.RTK_FORMAT_FILE['sfmeca'],
                         'sfmeca_format.xml')

        self.assertEqual(self.DUT.RTK_DATA_DIR, '/tmp/RTK/.config/RTK/data')
        self.assertEqual(self.DUT.RTK_ICON_DIR, '/tmp/RTK/.config/RTK/icons')
        self.assertEqual(self.DUT.RTK_LOG_DIR, '/tmp/RTK/.config/RTK/logs')
        self.assertEqual(self.DUT.RTK_PROG_DIR, '/home/arowland/analyses/rtk')

        self.assertEqual(self.DUT.RTK_PROG_INFO['host'], 'localhost')
        self.assertEqual(self.DUT.RTK_PROG_INFO['socket'], '3306')
        self.assertEqual(self.DUT.RTK_PROG_INFO['database'], '')
        self.assertEqual(self.DUT.RTK_PROG_INFO['user'], '')
        self.assertEqual(self.DUT.RTK_PROG_INFO['password'], '')

        self.assertEqual(self.DUT.RTK_BACKEND, 'sqlite')

        self.assertEqual(float(self.DUT.RTK_HR_MULTIPLIER), 1000000.0)
        self.assertEqual(int(self.DUT.RTK_DEC_PLACES), 6)
        self.assertEqual(float(self.DUT.RTK_MTIME), 100.0)
        self.assertEqual(int(self.DUT.RTK_MODE_SOURCE), 1)
        self.assertEqual(self.DUT.RTK_TABPOS['listbook'], 'bottom')
        self.assertEqual(self.DUT.RTK_TABPOS['modulebook'], 'top')
        self.assertEqual(self.DUT.RTK_TABPOS['workbook'], 'bottom')

    @attr(all=True, unit=True)
    def test06a_write_configuration(self):
        """
        (TestConfiguration) write_configuration should return False on success
        """

        self.DUT.RTK_SITE_DIR = dirname(dirname(__file__)) + '/config'
        self.DUT.RTK_HOME_DIR = '/tmp/RTK'
        self.DUT.set_site_variables()
        self.DUT.set_user_variables()
        self.DUT.create_user_configuration()

        # First, make sure everything is set to it's default value.
        self.assertEqual(self.DUT.RTK_PROG_INFO['host'], 'localhost')
        self.assertEqual(self.DUT.RTK_PROG_INFO['socket'], '3306')
        self.assertEqual(self.DUT.RTK_PROG_INFO['database'], '')
        self.assertEqual(self.DUT.RTK_PROG_INFO['user'], '')
        self.assertEqual(self.DUT.RTK_PROG_INFO['password'], '')
        self.assertEqual(self.DUT.RTK_BACKEND, '')
        self.assertEqual(float(self.DUT.RTK_HR_MULTIPLIER), 1000000.0)
        self.assertEqual(int(self.DUT.RTK_DEC_PLACES), 6)
        self.assertEqual(float(self.DUT.RTK_MTIME), 10.0)
        self.assertEqual(int(self.DUT.RTK_MODE_SOURCE), 1)
        self.assertEqual(self.DUT.RTK_TABPOS['listbook'], 'bottom')
        self.assertEqual(self.DUT.RTK_TABPOS['modulebook'], 'top')
        self.assertEqual(self.DUT.RTK_TABPOS['workbook'], 'bottom')

        # Next, programatically set these program constants.
        self.DUT.RTK_HR_MULTIPLIER = 1000.0
        self.DUT.RTK_MODE_SOURCE = 2
        self.DUT.RTK_TABPOS['listbook'] = 'top'
        self.DUT.RTK_TABPOS['modulebook'] = 'top'
        self.DUT.RTK_TABPOS['workbook'] = 'top'
        self.DUT.RTK_BACKEND = 'mysql'
        self.DUT.RTK_PROG_INFO['database'] = '/tmp/TestDB.rtk'
        self.DUT.RTK_PROG_INFO['user'] = 'arowland'

        # Write them to the RTK_PROG_CONF file and then re-read the file.
        self.assertFalse(self.DUT.write_configuration())
        self.assertFalse(self.DUT.read_configuration())

        # Verify that the constants were written/read properly.
        self.assertEqual(self.DUT.RTK_PROG_INFO['database'], '/tmp/TestDB.rtk')
        self.assertEqual(self.DUT.RTK_PROG_INFO['user'], 'arowland')
        self.assertEqual(self.DUT.RTK_BACKEND, 'mysql')
        self.assertEqual(float(self.DUT.RTK_HR_MULTIPLIER), 1000.0)
        self.assertEqual(int(self.DUT.RTK_MODE_SOURCE), 2)
        self.assertEqual(self.DUT.RTK_TABPOS['listbook'], 'top')
        self.assertEqual(self.DUT.RTK_TABPOS['modulebook'], 'top')
        self.assertEqual(self.DUT.RTK_TABPOS['workbook'], 'top')