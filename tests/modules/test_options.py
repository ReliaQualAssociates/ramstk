#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.modules.test_options.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Options class. """

from datetime import date, timedelta

import pytest

from rtk.dao import DAO
from rtk.modules.options import dtmOptions, dtcOptions
from rtk.modules.options.Model import (SiteOptionsDataModel,
                                       ProgramOptionsDataModel)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Andrew "weibullguy" Rowland'


@pytest.mark.integration
def test_create_options_data_model(test_dao, test_common_dao):
    """ __init__() should return an instance of the Options data model. """
    DUT = dtmOptions(test_dao, test_common_dao)

    assert isinstance(DUT, dtmOptions)
    assert isinstance(DUT.dao, DAO)
    assert isinstance(DUT.dtm_site_options, SiteOptionsDataModel)
    assert isinstance(DUT.dtm_program_options, ProgramOptionsDataModel)


@pytest.mark.integration
def test_do_select_all_site_info(test_dao, test_common_dao):
    """ do_select_all() should return None on success when selecting site Options. """
    DUT = dtmOptions(test_dao, test_common_dao)
    DUT.do_select_all(site_dao=test_common_dao, site=True, program=False)

    _attributes = DUT.site_options.get_attributes()
    assert _attributes['product_key'] == '0000'
    assert _attributes['expire_on'] == date.today() + timedelta(30)
    assert _attributes['function_enabled'] == 0
    assert _attributes['requirement_enabled'] == 0
    assert _attributes['hardware_enabled'] == 0
    assert _attributes['vandv_enabled'] == 0
    assert _attributes['fmea_enabled'] == 0


@pytest.mark.integration
def test_do_select_all_program_info(test_dao, test_common_dao):
    """ do_select_all() should return None on success when selecting program Options. """
    DUT = dtmOptions(test_dao, test_common_dao)
    DUT.do_select_all(site_dao=test_common_dao, site=False, program=True)

    _attributes = DUT.program_options.get_attributes()
    assert _attributes['function_active'] == 1
    assert _attributes['requirement_active'] == 1
    assert _attributes['hardware_active'] == 1
    assert _attributes['vandv_active'] == 1
    assert _attributes['method'] == 'STANDARD'
    assert _attributes['created_on'] == date.today()


@pytest.mark.integration
def test_do_update(test_dao, test_common_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmOptions(test_dao, test_common_dao)
    DUT.do_select_all(site_dao=test_common_dao, site=True, program=True)

    _attributes = DUT.program_options.get_attributes()
    _attributes['method'] == 'LRM'

    _attributes = DUT.site_options.get_attributes()
    _attributes['function_enabled'] == 1
    _attributes['requirement_enabled'] == 1
    _attributes['hardware_enabled'] == 1
    _attributes['vandv_enabled'] == 1
    _attributes['fmea_enabled'] == 1
    DUT.site_options.set_attributes(_attributes)

    assert not DUT.do_update()


@pytest.mark.integration
def test_create_options_data_controller(test_dao, test_common_dao,
                                        test_configuration):
    """ __init__() should return instance of Options data controller. """
    DUT = dtcOptions(
        test_dao, test_configuration, site_dao=test_common_dao, test='True')

    assert isinstance(DUT, dtcOptions)
    assert isinstance(DUT._dtm_data_model, dtmOptions)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_common_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKOptions data models. """
    DUT = dtcOptions(
        test_dao, test_configuration, site_dao=test_common_dao, test='True')

    assert not DUT.request_do_select_all(site=True, program=True)


@pytest.mark.integration
def test_request_get_options_site(test_dao, test_common_dao, test_configuration):
    """ request_get_options() should return a dict of site option:value pairs. """
    DUT = dtcOptions(
        test_dao, test_configuration, site_dao=test_common_dao, test='True')
    DUT.request_do_select_all(site=True, program=True)

    _options = DUT.request_get_options(site=True, program=False)

    assert isinstance(_options, dict)
    assert _options['function_enabled'] == 0
    assert _options['requirement_enabled'] == 0
    assert _options['hardware_enabled'] == 0
    assert _options['vandv_enabled'] == 0
    assert _options['fmea_enabled'] == 0


@pytest.mark.integration
def test_request_get_options_program(test_dao, test_common_dao, test_configuration):
    """ request_get_options() should return a dict of program option:value pairs. """
    DUT = dtcOptions(
        test_dao, test_configuration, site_dao=test_common_dao, test='True')
    DUT.request_do_select_all(site=True, program=True)

    _options = DUT.request_get_options(site=False, program=True)

    assert isinstance(_options, dict)
    assert _options['function_active'] == 1
    assert _options['requirement_active'] == 1
    assert _options['hardware_active'] == 1
    assert _options['vandv_active'] == 1
    assert _options['fmea_active'] == 1
    assert _options['created_by'] == ''
    assert _options['created_on'] == date.today()
    assert _options['last_saved_by'] == ''
    assert _options['last_saved'] == date.today()
    assert _options['method'] == 'STANDARD'


@pytest.mark.integration
def test_request_set_options_site(test_dao, test_common_dao, test_configuration):
    """ request_set_options() should return False when successfully setting site options. """
    DUT = dtcOptions(
        test_dao, test_configuration, site_dao=test_common_dao, test='True')
    DUT.request_do_select_all(site=True, program=True)

    _options = DUT.request_get_options(site=True, program=False)
    _options['function_enabled'] == 0

    (_error_code, _msg) = DUT.request_set_options(_options, site=True, program=False)

    assert _error_code == 0
    assert _msg == 'RAMSTK SUCCESS: Updating RAMSTKSiteInfo attributes.'

@pytest.mark.integration
def test_request_set_options_program(test_dao, test_common_dao, test_configuration):
    """ request_set_options() should return False when successfully setting program options. """
    DUT = dtcOptions(
        test_dao, test_configuration, site_dao=test_common_dao, test='True')
    DUT.request_do_select_all(site=True, program=True)

    _options = DUT.request_get_options(site=False, program=True)
    _options['function_active'] == 0

    (_error_code, _msg) = DUT.request_set_options(_options, site=False, program=True)

    assert _error_code == 0
    assert _msg == 'RAMSTK SUCCESS: Updating RAMSTKProgramInfo attributes.'


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_common_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcOptions(
        test_dao, test_configuration, site_dao=test_common_dao, test='True')
    DUT.request_do_select_all(site=True, program=True)

    assert not DUT.request_do_update()
