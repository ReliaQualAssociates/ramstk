# -*- coding: utf-8 -*-
#
#       tests.models.programdb.milhdbk217f.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK MIL-HDBK-217F module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMilHdbk217FRecord
from ramstk.models.dbtables import RAMSTKHardwareTable, RAMSTKMILHDBK217FTable
from tests import MockDAO


@pytest.fixture()
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _milhdbk217f_1 = RAMSTKMilHdbk217FRecord()
    _milhdbk217f_1.revision_id = 1
    _milhdbk217f_1.hardware_id = 1
    _milhdbk217f_1.A1 = 0.0
    _milhdbk217f_1.A2 = 0.0
    _milhdbk217f_1.B1 = 0.0
    _milhdbk217f_1.B2 = 0.0
    _milhdbk217f_1.C1 = 0.0
    _milhdbk217f_1.C2 = 0.0
    _milhdbk217f_1.lambdaBD = 0.0
    _milhdbk217f_1.lambdaBP = 0.0
    _milhdbk217f_1.lambdaCYC = 0.0
    _milhdbk217f_1.lambdaEOS = 0.0
    _milhdbk217f_1.piA = 0.0
    _milhdbk217f_1.piC = 0.0
    _milhdbk217f_1.piCD = 0.0
    _milhdbk217f_1.piCF = 0.0
    _milhdbk217f_1.piCR = 0.0
    _milhdbk217f_1.piCV = 0.0
    _milhdbk217f_1.piCYC = 0.0
    _milhdbk217f_1.piE = 0.0
    _milhdbk217f_1.piF = 0.0
    _milhdbk217f_1.piI = 0.0
    _milhdbk217f_1.piK = 0.0
    _milhdbk217f_1.piL = 0.0
    _milhdbk217f_1.piM = 0.0
    _milhdbk217f_1.piMFG = 0.0
    _milhdbk217f_1.piN = 0.0
    _milhdbk217f_1.piNR = 0.0
    _milhdbk217f_1.piP = 0.0
    _milhdbk217f_1.piPT = 0.0
    _milhdbk217f_1.piQ = 0.0
    _milhdbk217f_1.piR = 0.0
    _milhdbk217f_1.piS = 0.0
    _milhdbk217f_1.piT = 0.0
    _milhdbk217f_1.piTAPS = 0.0
    _milhdbk217f_1.piU = 0.0
    _milhdbk217f_1.piV = 0.0

    _milhdbk217f_2 = RAMSTKMilHdbk217FRecord()
    _milhdbk217f_2.revision_id = 1
    _milhdbk217f_2.hardware_id = 2
    _milhdbk217f_2.A1 = 0.0
    _milhdbk217f_2.A2 = 0.0
    _milhdbk217f_2.B1 = 0.0
    _milhdbk217f_2.B2 = 0.0
    _milhdbk217f_2.C1 = 0.0
    _milhdbk217f_2.C2 = 0.0
    _milhdbk217f_2.lambdaBD = 0.0
    _milhdbk217f_2.lambdaBP = 0.0
    _milhdbk217f_2.lambdaCYC = 0.0
    _milhdbk217f_2.lambdaEOS = 0.0
    _milhdbk217f_2.piA = 0.0
    _milhdbk217f_2.piC = 0.0
    _milhdbk217f_2.piCD = 0.0
    _milhdbk217f_2.piCF = 0.0
    _milhdbk217f_2.piCR = 0.0
    _milhdbk217f_2.piCV = 0.0
    _milhdbk217f_2.piCYC = 0.0
    _milhdbk217f_2.piE = 0.0
    _milhdbk217f_2.piF = 0.0
    _milhdbk217f_2.piI = 0.0
    _milhdbk217f_2.piK = 0.0
    _milhdbk217f_2.piL = 0.0
    _milhdbk217f_2.piM = 0.0
    _milhdbk217f_2.piMFG = 0.0
    _milhdbk217f_2.piN = 0.0
    _milhdbk217f_2.piNR = 0.0
    _milhdbk217f_2.piP = 0.0
    _milhdbk217f_2.piPT = 0.0
    _milhdbk217f_2.piQ = 0.0
    _milhdbk217f_2.piR = 0.0
    _milhdbk217f_2.piS = 0.0
    _milhdbk217f_2.piT = 0.0
    _milhdbk217f_2.piTAPS = 0.0
    _milhdbk217f_2.piU = 0.0
    _milhdbk217f_2.piV = 0.0

    _milhdbk217f_3 = RAMSTKMilHdbk217FRecord()
    _milhdbk217f_3.revision_id = 1
    _milhdbk217f_3.hardware_id = 3
    _milhdbk217f_3.A1 = 0.0
    _milhdbk217f_3.A2 = 0.0
    _milhdbk217f_3.B1 = 0.0
    _milhdbk217f_3.B2 = 0.0
    _milhdbk217f_3.C1 = 0.0
    _milhdbk217f_3.C2 = 0.0
    _milhdbk217f_3.lambdaBD = 0.0
    _milhdbk217f_3.lambdaBP = 0.0
    _milhdbk217f_3.lambdaCYC = 0.0
    _milhdbk217f_3.lambdaEOS = 0.0
    _milhdbk217f_3.piA = 0.0
    _milhdbk217f_3.piC = 0.0
    _milhdbk217f_3.piCD = 0.0
    _milhdbk217f_3.piCF = 0.0
    _milhdbk217f_3.piCR = 0.0
    _milhdbk217f_3.piCV = 0.0
    _milhdbk217f_3.piCYC = 0.0
    _milhdbk217f_3.piE = 0.0
    _milhdbk217f_3.piF = 0.0
    _milhdbk217f_3.piI = 0.0
    _milhdbk217f_3.piK = 0.0
    _milhdbk217f_3.piL = 0.0
    _milhdbk217f_3.piM = 0.0
    _milhdbk217f_3.piMFG = 0.0
    _milhdbk217f_3.piN = 0.0
    _milhdbk217f_3.piNR = 0.0
    _milhdbk217f_3.piP = 0.0
    _milhdbk217f_3.piPT = 0.0
    _milhdbk217f_3.piQ = 0.0
    _milhdbk217f_3.piR = 0.0
    _milhdbk217f_3.piS = 0.0
    _milhdbk217f_3.piT = 0.0
    _milhdbk217f_3.piTAPS = 0.0
    _milhdbk217f_3.piU = 0.0
    _milhdbk217f_3.piV = 0.0

    dao = MockDAO()
    dao.table = [
        _milhdbk217f_1,
        _milhdbk217f_2,
        _milhdbk217f_3,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of MIL-HDBK-217F attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "A1": 0.0,
        "A2": 0.0,
        "B1": 0.0,
        "B2": 0.0,
        "C1": 0.0,
        "C2": 0.0,
        "lambdaBD": 0.0,
        "lambdaBP": 0.0,
        "lambdaCYC": 0.0,
        "lambdaEOS": 0.0,
        "piA": 0.0,
        "piC": 0.0,
        "piCD": 0.0,
        "piCF": 0.0,
        "piCR": 0.0,
        "piCV": 0.0,
        "piCYC": 0.0,
        "piE": 0.0,
        "piF": 0.0,
        "piI": 0.0,
        "piK": 0.0,
        "piL": 0.0,
        "piM": 0.0,
        "piMFG": 0.0,
        "piN": 0.0,
        "piNR": 0.0,
        "piP": 0.0,
        "piPT": 0.0,
        "piQ": 0.0,
        "piR": 0.0,
        "piS": 0.0,
        "piT": 0.0,
        "piTAPS": 0.0,
        "piU": 0.0,
        "piV": 0.0,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMILHDBK217FTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_milhdbk217f")
    pub.unsubscribe(dut.do_update, "request_update_milhdbk217f")
    pub.unsubscribe(dut.do_get_tree, "request_get_milhdbk217f_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_milhdbk217f")
    pub.unsubscribe(dut.do_insert, "request_insert_milhdbk217f")
    pub.unsubscribe(dut._do_update_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut._do_update_tree, "succeed_insert_hardware")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_hardware_table(test_program_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHardwareTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hardware_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hardware_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_hardware")
    pub.unsubscribe(dut.do_update, "request_update_hardware")
    pub.unsubscribe(dut.do_get_tree, "request_get_hardware_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_hardware")
    pub.unsubscribe(dut.do_insert, "request_insert_hardware")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMILHDBK217FTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_milhdbk217f")
    pub.unsubscribe(dut.do_update, "request_update_milhdbk217f")
    pub.unsubscribe(dut.do_get_tree, "request_get_milhdbk217f_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_milhdbk217f")
    pub.unsubscribe(dut.do_insert, "request_insert_milhdbk217f")
    pub.unsubscribe(dut._do_update_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut._do_update_tree, "succeed_insert_hardware")

    # Delete the device under test.
    del dut
