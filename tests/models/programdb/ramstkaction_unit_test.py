# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkaction_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKAction module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKAction


@pytest.fixture
def mock_program_dao(monkeypatch):
    _action_1 = RAMSTKAction()
    _action_1.revision_id = 1
    _action_1.hardware_id = 1
    _action_1.mode_id = 6
    _action_1.mechanism_id = 3
    _action_1.cause_id = 1
    _action_1.action_id = 1
    _action_1.action_due_date = date(2019, 8, 20)
    _action_1.action_approve_date = date(2019, 8, 20)
    _action_1.action_status = ""
    _action_1.action_closed = 0
    _action_1.action_taken = ""
    _action_1.action_close_date = date(2019, 8, 20)
    _action_1.action_recommended = "Recommended action #1 for Failure Cause #1"
    _action_1.action_category = ""
    _action_1.action_owner = ""
    _action_1.action_approved = 0

    _action_2 = RAMSTKAction()
    _action_2.revision_id = 1
    _action_2.hardware_id = 1
    _action_2.mode_id = 6
    _action_2.mechanism_id = 3
    _action_2.cause_id = 2
    _action_2.action_id = 2
    _action_2.action_due_date = date(2019, 8, 20)
    _action_2.action_approve_date = date(2019, 8, 20)
    _action_2.action_status = ""
    _action_2.action_closed = 0
    _action_2.action_taken = ""
    _action_2.action_close_date = date(2019, 8, 20)
    _action_2.action_recommended = "Recommended action #2 for Failure Cause #1"
    _action_2.action_category = ""
    _action_2.action_owner = ""
    _action_2.action_approved = 0

    DAO = MockDAO()
    DAO.table = [
        _action_1,
        _action_2,
    ]

    yield DAO


@pytest.fixture
def test_attributes(monkeypatch):
    """Set attributes dict to use for tests."""

    yield {
        "action_due_date": date(2019, 8, 23),
        "action_approve_date": date(2019, 8, 22),
        "action_status": "Closed",
        "action_closed": 1,
        "action_taken": "None",
        "action_close_date": date(2019, 8, 21),
        "action_recommended": "Recommended action for Failure Cause #1",
        "action_category": "Important category",
        "action_owner": "Me",
        "action_approved": 1,
    }


@pytest.mark.usefixtures("mock_program_dao", "test_attributes")
class TestRAMSTKAction:
    """Class for testing the RAMSTKAction model."""

    @pytest.mark.unit
    def test_ramstkaction_create(self, mock_program_dao):
        """should create an instance of the model."""
        DUT = RAMSTKAction()

        assert DUT.__tablename__ == "ramstk_action"
        assert DUT.revision_id is None
        assert DUT.hardware_id is None
        assert DUT.mode_id is None
        assert DUT.mechanism_id is None
        assert DUT.cause_id is None
        assert DUT.action_id is None
        assert DUT.action_recommended is None
        assert DUT.action_category is None
        assert DUT.action_owner is None
        assert DUT.action_due_date is None
        assert DUT.action_status is None
        assert DUT.action_taken is None
        assert DUT.action_approved is None
        assert DUT.action_approve_date is None
        assert DUT.action_closed is None
        assert DUT.action_close_date is None

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """should return a dict of attribute:value pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["action_due_date"] == date(2019, 8, 20)
        assert _attributes["action_approve_date"] == date(2019, 8, 20)
        assert _attributes["action_status"] == ""
        assert _attributes["action_closed"] == 0
        assert _attributes["action_taken"] == ""
        assert _attributes["action_close_date"] == date(2019, 8, 20)
        assert (
            _attributes["action_recommended"] == "Recommended action #1 for "
            "Failure Cause #1"
        )
        assert _attributes["action_category"] == ""
        assert _attributes["action_owner"] == ""
        assert _attributes["action_approved"] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao, test_attributes):
        """should return None on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        assert DUT.set_attributes(test_attributes) is None
        assert DUT.action_due_date == date(2019, 8, 23)
        assert DUT.action_approve_date == date(2019, 8, 22)
        assert DUT.action_status == "Closed"
        assert DUT.action_closed == 1
        assert DUT.action_taken == "None"
        assert DUT.action_close_date == date(2019, 8, 21)
        assert DUT.action_recommended == "Recommended action for Failure Cause #1"
        assert DUT.action_category == "Important category"
        assert DUT.action_owner == "Me"
        assert DUT.action_approved == 1

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao, test_attributes):
        """should set an attribute to it's default value when the a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        test_attributes["action_status"] = None

        assert DUT.set_attributes(test_attributes) is None
        assert DUT.get_attributes()["action_recommended"] == (
            "Recommended action for Failure Cause #1"
        )
        assert DUT.get_attributes()["action_status"] == ""

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """should raise an AttributeError when passed an unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({"shibboly-bibbly-boo": 0.9998})
