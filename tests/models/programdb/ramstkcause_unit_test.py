# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkcause_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKCause module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKCause


@pytest.fixture
def mock_program_dao(monkeypatch):
    _cause_1 = RAMSTKCause()
    _cause_1.revision_id = 1
    _cause_1.hardware_id = 1
    _cause_1.mode_id = 6
    _cause_1.mechanism_id = 3
    _cause_1.cause_id = 1
    _cause_1.description = "Test Failure Cause #1"
    _cause_1.rpn = 100
    _cause_1.rpn_new = 100
    _cause_1.rpn_detection = 10
    _cause_1.rpn_detection_new = 10
    _cause_1.rpn_occurrence_new = 10
    _cause_1.rpn_occurrence = 10

    _cause_2 = RAMSTKCause()
    _cause_2.revision_id = 1
    _cause_2.hardware_id = 1
    _cause_2.mode_id = 6
    _cause_2.mechanism_id = 3
    _cause_2.cause_id = 2
    _cause_2.description = "Test Failure Cause #2"
    _cause_2.rpn = 100
    _cause_2.rpn_new = 100
    _cause_2.rpn_detection = 10
    _cause_2.rpn_detection_new = 10
    _cause_2.rpn_occurrence_new = 10
    _cause_2.rpn_occurrence = 10

    DAO = MockDAO()
    DAO.table = [
        _cause_1,
        _cause_2,
    ]

    yield DAO


ATTRIBUTES = {
    "rpn_new": 40,
    "rpn_occurrence_new": 5,
    "description": "Test Failure Cause #1 for Failure Mechanism #3",
    "rpn_occurrence": 10,
    "rpn_detection_new": 8,
    "rpn_detection": 10,
    "rpn": 100,
}


@pytest.mark.usefixtures("mock_program_dao")
class TestRAMSTKCause:
    """Class for testing the RAMSTKCause model."""

    @pytest.mark.unit
    def test_ramstkcause_create(self, mock_program_dao):
        """should return a RAMSTKCause instance."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        assert isinstance(DUT, RAMSTKCause)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == "ramstk_cause"
        assert DUT.revision_id == 1
        assert DUT.hardware_id == 1
        assert DUT.mode_id == 6
        assert DUT.mechanism_id == 3
        assert DUT.cause_id == 1
        assert DUT.description == "Test Failure Cause #1"
        assert DUT.rpn == 100
        assert DUT.rpn_detection == 10
        assert DUT.rpn_detection_new == 10
        assert DUT.rpn_new == 100
        assert DUT.rpn_occurrence == 10
        assert DUT.rpn_occurrence_new == 10

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """should return a dict of attribute key:value pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["mode_id"] == 6
        assert _attributes["mechanism_id"] == 3
        assert _attributes["cause_id"] == 1
        assert _attributes["description"] == ("Test Failure Cause #1")
        assert _attributes["rpn"] == 100
        assert _attributes["rpn_detection"] == 10
        assert _attributes["rpn_detection_new"] == 10
        assert _attributes["rpn_new"] == 100
        assert _attributes["rpn_occurrence"] == 10
        assert _attributes["rpn_occurrence_new"] == 10

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """should return None on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.description == "Test Failure Cause #1 for Failure Mechanism #3"
        assert DUT.rpn == 100
        assert DUT.rpn_detection == 10
        assert DUT.rpn_detection_new == 8
        assert DUT.rpn_new == 40
        assert DUT.rpn_occurrence == 10
        assert DUT.rpn_occurrence_new == 5

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """should set an attribute to it's default value when passed a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        ATTRIBUTES["description"] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()["description"] == ""

    @pytest.mark.unit
    def test_set_attributes_unknown_attribute(self, mock_program_dao):
        """should raise an AttributeError when passed an unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({"shibboly-bibbly-boo": 0.9998})
