# pylint: disable=protected-access, missing-docstring, no-self-use
# -*- coding: utf-8 -*-
#
#       tests.db.test_common.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for common database methods and operations."""

# Standard Library Imports
import os
import tempfile
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from sqlalchemy import MetaData, create_engine, event, exc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

# RAMSTK Package Imports
from mock import patch
from ramstk.db.base import BaseDatabase
from ramstk.db.common import (
    _load_fmea_tables, _load_hazard_analysis_tables,
    _load_incident_report_tables, _load_miscellaneous_tables,
    _load_pof_tables, _load_site_info, do_add_administrator,
    do_create_common_db, do_make_commondb_tables
)
from ramstk.exceptions import DataAccessError
from ramstk.models.commondb import RAMSTKSiteInfo, RAMSTKUser
from ramstk.models.programdb import RAMSTKFunction, RAMSTKRevision

TEST_COMMON_DB = BaseDatabase()
TEST_COMMON_DB.do_connect('sqlite:///:memory:')


def on_fail_read_license(error_message):
    assert error_message == ('Unable to read license key file.  Defaulting '
                             'to a 30-day demo license.')
    print("\033[35m\nfail_read_license topic was broadcast.")


def test_create_common_db_tables():
    """do_make_commondb_tables() should return None when successfully creating the tables in the RAMSTK common database."""
    assert do_make_commondb_tables(TEST_COMMON_DB.engine) is None
    assert TEST_COMMON_DB.do_insert(RAMSTKSiteInfo()) is None
    assert TEST_COMMON_DB.get_last_id('ramstk_site_info', 'fld_site_id') == 1


@pytest.mark.usefixtures('test_license_file')
def test_load_site_info_with_license(test_license_file):
    """_load_site_info() should return None and load the license key information when a license key file can be read."""
    assert _load_site_info(TEST_COMMON_DB.session) is None

    # Retrieve the newly create site info record (note this is site ID=2 as the
    # _load_site_info() function creates a new record).  Generally we won't be
    # inserting a record before calling the _load_site_info() function, it just
    # so happens we do here because of the ordering of tests.
    _record = TEST_COMMON_DB.session.query(RAMSTKSiteInfo).filter(
        RAMSTKSiteInfo.site_id == 2).first()
    assert _record.product_key == 'apowdigfb3rh9214839qu'
    assert _record.expire_on == date(2019, 8, 7)


def test_load_site_info_no_license():
    """_load_site_info() should return None and load the default 30-day license when the license key file can't be read."""
    pub.subscribe(on_fail_read_license, 'fail_read_license')

    assert _load_site_info(TEST_COMMON_DB.session) is None

    # Retrieve the newly create site info record (note this is site ID=3 as the
    # _load_site_info() function creates a new record).  Generally we won't be
    # inserting records before calling the _load_site_info() function, it just
    # so happens we do here because of the ordering of tests.
    _record = TEST_COMMON_DB.session.query(RAMSTKSiteInfo).filter(
        RAMSTKSiteInfo.site_id == 3).first()
    assert _record.product_key == '0000'
    assert _record.expire_on == date.today() + timedelta(days=30)

    pub.unsubscribe(on_fail_read_license, 'fail_read_license')


def test_load_miscellaneous_tables():
    """_load_miscellaneous_tables() should return None when successfully populating the miscellaneous tables."""
    assert _load_miscellaneous_tables(TEST_COMMON_DB.session) is None


def test_load_fmea_tables():
    """_load_fmea_tables() should return None when successfully populating the FMEA-related tables."""
    assert _load_fmea_tables(TEST_COMMON_DB.session) is None


def test_load_hazard_analysis_tables():
    """_load_hazard_analysis_tables() should return None when successfully populating the FHA-related tables."""
    assert _load_hazard_analysis_tables(TEST_COMMON_DB.session) is None


def test_load_incident_report_tables():
    """_load_incident_report_tables() should return None when successfully populating the incident report related tables."""
    assert _load_incident_report_tables(TEST_COMMON_DB.session) is None


def test_load_pof_tables():
    """_load_pof_tables() should return None when successfully populating the PoF-related tables."""
    assert _load_pof_tables(TEST_COMMON_DB.session) is None


@patch('builtins.input', side_effect=['y', 'tester', 'johnny', 'johnny.tester@reliaqual.com', '+1.269.867.5309'])
def test_do_add_administrator(inputs):
    """do_add_administrator() should return None when successfully adding an administrative user to the RAMSTKUser table."""
    assert do_add_administrator(TEST_COMMON_DB.session) is None


@patch('builtins.input', return_value='n')
def test_do_add_administrator_choose_no(inputs):
    """do_add_administrator() should return None when choosing not to add an administrative user to the RAMSTKUser table."""
    assert do_add_administrator(TEST_COMMON_DB.session) is None


@patch('builtins.input', side_effect=['y', 'tester', 'johnny', 'johnny.tester@reliaqual.com', '+1.269.867.5309'])
def test_do_create_common_db(monkeypatch):
    """do_create_common_db() should return None when successfully creating a RAMSTK common database."""
    TEST_COMMON_DB.do_disconnect()
    TEST_COMMON_DB.do_connect('sqlite:///:memory:')

    assert do_create_common_db(TEST_COMMON_DB.engine, TEST_COMMON_DB.session) is None
    _record = TEST_COMMON_DB.session.query(RAMSTKUser).filter(
        RAMSTKUser.user_id == 1).first()
    assert _record.user_lname == 'tester'
    assert _record.user_fname == 'johnny'
    assert _record.user_email == 'johnny.tester@reliaqual.com'
    assert _record.user_phone == '+1.269.867.5309'
