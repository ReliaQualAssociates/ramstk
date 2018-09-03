#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.unit.TestConfiguration.py is part of The RAMSTK Project
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
"""
This is the test class for testing the Configuration module algorithms and
models.
"""

import shutil
import sys
from os import environ, makedirs, name
from os.path import dirname, isfile

sys.path.insert(
    0,
    dirname(dirname(__file__)) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

from Configuration import Configuration

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2016 Andrew "Weibullguy" Rowland'


class TestConfiguration(unittest.TestCase):
    """
    Class for testing the RAMSTK Configuration.
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
            makedirs('/tmp/RAMSTK/data')
        except OSError:
            pass
        try:
            makedirs('/tmp/RAMSTK/icons')
        except OSError:
            pass
        try:
            makedirs('/tmp/RAMSTK/logs')
        except OSError:
            pass

    @attr(all=True, unit=True)
    def test00_initialize_configuration(self):
        """
        (TestConfiguration) __init__ should create an instance of the Configuration object when initializing
        """

        self.assertTrue(isinstance(self.DUT, Configuration))

        self.assertEqual(self.DUT.RAMSTK_MODE, '')
        self.assertEqual(self.DUT.RAMSTK_SITE_CONF, '')
        self.assertEqual(self.DUT.RAMSTK_PROG_CONF, '')
        self.assertEqual(self.DUT.RAMSTK_DEBUG_LOG, '')
        self.assertEqual(self.DUT.RAMSTK_IMPORT_LOG, '')
        self.assertEqual(self.DUT.RAMSTK_USER_LOG, '')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE, {})
        self.assertEqual(self.DUT.RAMSTK_COLORS, {})
        self.assertEqual(self.DUT.RAMSTK_PREFIX, {})
        self.assertEqual(self.DUT.RAMSTK_ACTION_CATEGORY, {})
        self.assertEqual(self.DUT.RAMSTK_INCIDENT_CATEGORY, {})
        self.assertEqual(self.DUT.RAMSTK_SEVERITY, {})
        self.assertEqual(self.DUT.RAMSTK_ACTIVE_ENVIRONMENTS, {})
        self.assertEqual(self.DUT.RAMSTK_DORMANT_ENVIRONMENTS, {})
        self.assertEqual(self.DUT.RAMSTK_SW_DEV_ENVIRONMENTS, {})
        self.assertEqual(self.DUT.RAMSTK_AFFINITY_GROUPS, {})
        self.assertEqual(self.DUT.RAMSTK_WORKGROUPS, {})
        self.assertEqual(self.DUT.RAMSTK_FAILURE_PROBABILITY, {})
        self.assertEqual(self.DUT.RAMSTK_SW_LEVELS, {})
        self.assertEqual(self.DUT.RAMSTK_DETECTION_METHODS, {})
        self.assertEqual(self.DUT.RAMSTK_SW_TEST_METHODS, {})
        self.assertEqual(self.DUT.RAMSTK_ALLOCATION_MODELS, {})
        self.assertEqual(self.DUT.RAMSTK_DAMAGE_MODELS, {})
        self.assertEqual(self.DUT.RAMSTK_HR_MODEL, {})
        self.assertEqual(self.DUT.RAMSTK_LIFECYCLE, {})
        self.assertEqual(self.DUT.RAMSTK_SW_DEV_PHASES, {})
        self.assertEqual(self.DUT.RAMSTK_RPN_DETECTION, {})
        self.assertEqual(self.DUT.RAMSTK_RPN_SEVERITY, {})
        self.assertEqual(self.DUT.RAMSTK_RPN_OCCURRENCE, {})
        self.assertEqual(self.DUT.RAMSTK_ACTION_STATUS, {})
        self.assertEqual(self.DUT.RAMSTK_INCIDENT_STATUS, {})
        self.assertEqual(self.DUT.RAMSTK_CONTROL_TYPES, [])
        self.assertEqual(self.DUT.RAMSTK_COST_TYPE, {})
        self.assertEqual(self.DUT.RAMSTK_HR_TYPE, {})
        self.assertEqual(self.DUT.RAMSTK_INCIDENT_TYPE, {})
        self.assertEqual(self.DUT.RAMSTK_MTTR_TYPE, {})
        self.assertEqual(self.DUT.RAMSTK_REQUIREMENT_TYPE, {})
        self.assertEqual(self.DUT.RAMSTK_VALIDATION_TYPE, {})
        self.assertEqual(self.DUT.RAMSTK_SW_APPLICATION, {})
        self.assertEqual(self.DUT.RAMSTK_CATEGORIES, {})
        self.assertEqual(self.DUT.RAMSTK_CRITICALITY, {})
        self.assertEqual(self.DUT.RAMSTK_FAILURE_MODES, {})
        self.assertEqual(self.DUT.RAMSTK_HAZARDS, {})
        self.assertEqual(self.DUT.RAMSTK_MANUFACTURERS, {})
        self.assertEqual(self.DUT.RAMSTK_MEASUREMENT_UNITS, {})
        self.assertEqual(self.DUT.RAMSTK_OPERATING_PARAMETERS, {})
        self.assertEqual(self.DUT.RAMSTK_S_DIST, {})
        self.assertEqual(self.DUT.RAMSTK_STAKEHOLDERS, {})
        self.assertEqual(self.DUT.RAMSTK_SUBCATEGORIES, {})
        self.assertEqual(self.DUT.RAMSTK_USERS, {})
        self.assertEqual(self.DUT.RAMSTK_RISK_POINTS, [4, 10])
        self.assertEqual(self.DUT.RAMSTK_MODE_SOURCE, 1)
        self.assertEqual(self.DUT.RAMSTK_FMECA_METHOD, 1)
        self.assertEqual(self.DUT.RAMSTK_RPN_FORMAT, 0)
        self.assertEqual(self.DUT.RAMSTK_COM_BACKEND, '')
        self.assertEqual(self.DUT.RAMSTK_BACKEND, '')
        self.assertEqual(self.DUT.RAMSTK_COM_INFO, {})
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO, {})
        self.assertEqual(self.DUT.RAMSTK_MODULES, {})
        self.assertEqual(self.DUT.RAMSTK_PAGE_NUMBER, {})
        self.assertEqual(self.DUT.RAMSTK_HR_MULTIPLIER, 1000000.0)
        self.assertEqual(self.DUT.RAMSTK_DEC_PLACES, 6)
        self.assertEqual(self.DUT.RAMSTK_MTIME, 10.0)
        self.assertEqual(self.DUT.RAMSTK_TABPOS, {
            'listbook': 'top',
            'modulebook': 'bottom',
            'workbook': 'bottom'
        })
        self.assertEqual(self.DUT.RAMSTK_GUI_LAYOUT, 'advanced')
        self.assertEqual(self.DUT.RAMSTK_METHOD, 'STANDARD')

        if name == 'posix':
            self.assertEqual(self.DUT.RAMSTK_OS, 'Linux')
            self.assertEqual(self.DUT.RAMSTK_LOCALE, 'en_US')
            self.assertEqual(self.DUT.RAMSTK_SITE_DIR, '/etc/RAMSTK')
            self.assertEqual(self.DUT.RAMSTK_HOME_DIR, environ['HOME'])
            self.assertEqual(self.DUT.RAMSTK_DATA_DIR, '/usr/share/RAMSTK')
            self.assertEqual(self.DUT.RAMSTK_ICON_DIR, '/usr/share/pixmaps/RAMSTK')
            self.assertEqual(self.DUT.RAMSTK_LOG_DIR, '/var/log/RAMSTK')
            self.assertEqual(self.DUT.RAMSTK_PROG_DIR,
                             self.DUT.RAMSTK_HOME_DIR + '/analyses/rtk')
            self.assertEqual(self.DUT.RAMSTK_CONF_DIR, '')

    @attr(all=True, unit=True)
    def test01a_set_site_variables(self):
        """
        (TestConfiguration) set_site_variables should return False on success
        """

        self.assertFalse(self.DUT.set_site_variables())

        if name == 'posix':
            self.assertEqual(self.DUT.RAMSTK_SITE_DIR, '/etc/RAMSTK')
            self.assertEqual(self.DUT.RAMSTK_HOME_DIR, environ['HOME'])
            self.assertEqual(self.DUT.RAMSTK_CONF_DIR,
                             self.DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK')
            self.assertEqual(self.DUT.RAMSTK_DATA_DIR,
                             self.DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK/data')
            self.assertEqual(self.DUT.RAMSTK_ICON_DIR,
                             self.DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK/icons')
            self.assertEqual(self.DUT.RAMSTK_LOG_DIR,
                             self.DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK/logs')
            self.assertEqual(self.DUT.RAMSTK_PROG_DIR,
                             self.DUT.RAMSTK_HOME_DIR + '/analyses/rtk')
            self.assertEqual(self.DUT.RAMSTK_SITE_CONF,
                             self.DUT.RAMSTK_CONF_DIR + '/site.conf')

    @attr(all=True, unit=True)
    def test02a_set_user_variables(self):
        """
        (TestConfiguration) set_user_variables should return False on success
        """

        self.assertFalse(self.DUT.set_user_variables())

        self.assertEqual(self.DUT.RAMSTK_PROG_CONF,
                         self.DUT.RAMSTK_CONF_DIR + '/RAMSTK.conf')

    @attr(all=True, unit=True)
    def test03a_create_site_configuration(self):
        """
        (TestConfiguration) _create_site_configuration should return False on success
        """

        self.DUT.RAMSTK_SITE_DIR = '/tmp/RAMSTK'
        self.DUT.RAMSTK_HOME_DIR = '/tmp/RAMSTK'
        self.DUT.RAMSTK_SITE_CONF = self.DUT.RAMSTK_SITE_DIR + '/site.conf'

        self.assertFalse(self.DUT._create_site_configuration())
        self.assertTrue(isfile('/tmp/RAMSTK/site.conf'))

    @attr(all=True, unit=True)
    def test04a_create_user_configuration(self):
        """
        (TestConfiguration) create_user_configuration should return False on success
        """

        self.DUT.RAMSTK_SITE_DIR = dirname(dirname(__file__)) + '/config'
        self.DUT.RAMSTK_HOME_DIR = '/tmp/RAMSTK'
        self.DUT.set_site_variables()
        self.DUT.set_user_variables()

        self.assertFalse(self.DUT.create_user_configuration())
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/RAMSTK.conf'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/alt_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/dataset_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/ffmeca_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/fmeca_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/fraca_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/function_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/hardware_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/incident_format.xml'))
        self.assertTrue(
            isfile(self.DUT.RAMSTK_CONF_DIR + '/mechanisms_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/modes_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/part_format.xml'))
        self.assertTrue(
            isfile(self.DUT.RAMSTK_CONF_DIR + '/requirement_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/revision_format.xml'))
        self.assertTrue(
            isfile(self.DUT.RAMSTK_CONF_DIR + '/rgincident_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/risk_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/sfmeca_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/sia_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/software_format.xml'))
        self.assertTrue(
            isfile(self.DUT.RAMSTK_CONF_DIR + '/stakeholder_format.xml'))
        self.assertTrue(isfile(self.DUT.RAMSTK_CONF_DIR + '/testing_format.xml'))
        self.assertTrue(
            isfile(self.DUT.RAMSTK_CONF_DIR + '/validation_format.xml'))

    @attr(all=True, unit=True)
    def test05a_read_site_configuration(self):
        """
        (TestConfiguration) _read_site_configuration should return False on success
        """

        self.DUT.RAMSTK_SITE_DIR = dirname(dirname(__file__)) + '/config'
        self.DUT.RAMSTK_HOME_DIR = '/tmp/RAMSTK'
        self.DUT.set_site_variables()
        self.DUT.set_user_variables()
        self.DUT.create_user_configuration()

        self.assertFalse(self.DUT._read_site_configuration())

        self.assertEqual(self.DUT.RAMSTK_COM_BACKEND, 'sqlite')
        self.assertEqual(self.DUT.RAMSTK_COM_INFO['host'], 'localhost')
        self.assertEqual(self.DUT.RAMSTK_COM_INFO['socket'], '3306')
        self.assertEqual(self.DUT.RAMSTK_COM_INFO['database'], '')
        self.assertEqual(self.DUT.RAMSTK_COM_INFO['user'], 'user')
        self.assertEqual(self.DUT.RAMSTK_COM_INFO['password'], 'password')

    @attr(all=True, unit=True)
    def test05b_read_configuration(self):
        """
        (TestConfiguration) read_configuration should return False on success
        """

        self.DUT.RAMSTK_SITE_DIR = dirname(dirname(__file__)) + '/config'
        self.DUT.RAMSTK_HOME_DIR = '/tmp/RAMSTK'
        self.DUT.set_site_variables()
        self.DUT.set_user_variables()
        self.DUT.create_user_configuration()

        self.assertFalse(self.DUT.read_configuration())
        self.assertEqual(self.DUT.RAMSTK_COLORS['revisionfg'], '#000000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['functionfg'], '#0000FF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['requirementfg'], '#000000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['assemblyfg'], '#000000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['partfg'], '#000000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['overstressfg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['taggedfg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['nofrmodelfg'], '#A52A2A')
        self.assertEqual(self.DUT.RAMSTK_COLORS['softwarefg'], '#000000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['incidentfg'], '#000000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['validationfg'], '#00FF00')
        self.assertEqual(self.DUT.RAMSTK_COLORS['testfg'], '#000000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['survivalfg'], '#000000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['revisionbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['functionbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['requirementbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['assemblybg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['partbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['overstressbg'], '#FF0000')
        self.assertEqual(self.DUT.RAMSTK_COLORS['taggedbg'], '#00FF00')
        self.assertEqual(self.DUT.RAMSTK_COLORS['softwarebg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['incidentbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['validationbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['testbg'], '#FFFFFF')
        self.assertEqual(self.DUT.RAMSTK_COLORS['survivalbg'], '#FFFFFF')

        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['revision'],
                         'revision_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['function'],
                         'function_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['requirement'],
                         'requirement_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['hardware'],
                         'hardware_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['software'],
                         'software_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['incident'],
                         'incident_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['validation'],
                         'validation_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['testing'],
                         'testing_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['part'], 'part_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['sia'], 'sia_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['fmeca'], 'fmeca_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['rgincident'],
                         'rgincident_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['stakeholder'],
                         'stakeholder_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['dataset'],
                         'dataset_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['risk'], 'risk_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['ffmeca'],
                         'ffmeca_format.xml')
        self.assertEqual(self.DUT.RAMSTK_FORMAT_FILE['sfmeca'],
                         'sfmeca_format.xml')

        self.assertEqual(self.DUT.RAMSTK_DATA_DIR, '/tmp/RAMSTK/.config/RAMSTK/data')
        self.assertEqual(self.DUT.RAMSTK_ICON_DIR, '/tmp/RAMSTK/.config/RAMSTK/icons')
        self.assertEqual(self.DUT.RAMSTK_LOG_DIR, '/tmp/RAMSTK/.config/RAMSTK/logs')
        self.assertEqual(self.DUT.RAMSTK_PROG_DIR, '/home/arowland/analyses/rtk')

        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['host'], 'localhost')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['socket'], '3306')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['database'], '')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['user'], '')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['password'], '')

        self.assertEqual(self.DUT.RAMSTK_BACKEND, 'sqlite')

        self.assertEqual(float(self.DUT.RAMSTK_HR_MULTIPLIER), 1000000.0)
        self.assertEqual(int(self.DUT.RAMSTK_DEC_PLACES), 6)
        self.assertEqual(float(self.DUT.RAMSTK_MTIME), 100.0)
        self.assertEqual(int(self.DUT.RAMSTK_MODE_SOURCE), 1)
        self.assertEqual(self.DUT.RAMSTK_TABPOS['listbook'], 'bottom')
        self.assertEqual(self.DUT.RAMSTK_TABPOS['modulebook'], 'top')
        self.assertEqual(self.DUT.RAMSTK_TABPOS['workbook'], 'bottom')

    @attr(all=True, unit=True)
    def test06a_write_configuration(self):
        """
        (TestConfiguration) write_configuration should return False on success
        """

        self.DUT.RAMSTK_SITE_DIR = dirname(dirname(__file__)) + '/config'
        self.DUT.RAMSTK_HOME_DIR = '/tmp/RAMSTK'
        self.DUT.set_site_variables()
        self.DUT.set_user_variables()
        self.DUT.create_user_configuration()

        # First, make sure everything is set to it's default value.
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['host'], 'localhost')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['socket'], '3306')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['database'], '')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['user'], '')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['password'], '')
        self.assertEqual(self.DUT.RAMSTK_BACKEND, '')
        self.assertEqual(float(self.DUT.RAMSTK_HR_MULTIPLIER), 1000000.0)
        self.assertEqual(int(self.DUT.RAMSTK_DEC_PLACES), 6)
        self.assertEqual(float(self.DUT.RAMSTK_MTIME), 10.0)
        self.assertEqual(int(self.DUT.RAMSTK_MODE_SOURCE), 1)
        self.assertEqual(self.DUT.RAMSTK_TABPOS['listbook'], 'bottom')
        self.assertEqual(self.DUT.RAMSTK_TABPOS['modulebook'], 'top')
        self.assertEqual(self.DUT.RAMSTK_TABPOS['workbook'], 'bottom')

        # Next, programatically set these program constants.
        self.DUT.RAMSTK_HR_MULTIPLIER = 1000.0
        self.DUT.RAMSTK_MODE_SOURCE = 2
        self.DUT.RAMSTK_TABPOS['listbook'] = 'top'
        self.DUT.RAMSTK_TABPOS['modulebook'] = 'top'
        self.DUT.RAMSTK_TABPOS['workbook'] = 'top'
        self.DUT.RAMSTK_BACKEND = 'mysql'
        self.DUT.RAMSTK_PROG_INFO['database'] = '/tmp/TestDB.rtk'
        self.DUT.RAMSTK_PROG_INFO['user'] = 'arowland'

        # Write them to the RAMSTK_PROG_CONF file and then re-read the file.
        self.assertFalse(self.DUT.write_configuration())
        self.assertFalse(self.DUT.read_configuration())

        # Verify that the constants were written/read properly.
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['database'], '/tmp/TestDB.rtk')
        self.assertEqual(self.DUT.RAMSTK_PROG_INFO['user'], 'arowland')
        self.assertEqual(self.DUT.RAMSTK_BACKEND, 'mysql')
        self.assertEqual(float(self.DUT.RAMSTK_HR_MULTIPLIER), 1000.0)
        self.assertEqual(int(self.DUT.RAMSTK_MODE_SOURCE), 2)
        self.assertEqual(self.DUT.RAMSTK_TABPOS['listbook'], 'top')
        self.assertEqual(self.DUT.RAMSTK_TABPOS['modulebook'], 'top')
        self.assertEqual(self.DUT.RAMSTK_TABPOS['workbook'], 'top')
