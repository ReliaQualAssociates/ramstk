# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.test_utilities.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Utilities module algorithms and models."""

# Standard Library Imports
import logging

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk import RAMSTKLogManager


class TestLogManager:
    """Test class for RAMSTKLogManager methods."""
    def test_create_log_manager(self):
        """__init__() should create an instance of the RAMSTKLogManager."""
        _testlog = './test_info.log'

        DUT = RAMSTKLogManager(_testlog)

        assert isinstance(DUT, RAMSTKLogManager)
        assert isinstance(DUT.loggers['ramstk.logger'], logging.Logger)
        assert DUT.log_file == _testlog
        assert pub.isSubscribed(DUT._do_log_fail_message, 'fail_delete_fmea')
        assert pub.isSubscribed(DUT._do_log_fail_message, 'fail_insert_action')
        assert pub.isSubscribed(DUT._do_log_fail_message, 'fail_insert_cause')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_control')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_mechanism')
        assert pub.isSubscribed(DUT._do_log_fail_message, 'fail_insert_mode')
        assert pub.isSubscribed(DUT._do_log_fail_message, 'fail_update_fmea')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_delete_function')
        assert pub.isSubscribed(DUT._do_log_fail_message, 'fail_delete_hazard')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_function')
        assert pub.isSubscribed(DUT._do_log_fail_message, 'fail_insert_hazard')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_update_function')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_hardware')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_validation')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_stakeholder')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_revision')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_environment')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_failure_definition')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_mission')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_mission_phase')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_requirement')
        assert pub.isSubscribed(DUT._do_log_fail_message, 'fail_insert_opload')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_opstress')
        assert pub.isSubscribed(DUT._do_log_fail_message,
                                'fail_insert_test_method')

    @pytest.mark.unit
    def test_log_fail_messages(self):
        """_do_log_fail_message() should be called when fail_* messages are broadcast and log the associated error message."""
        _testlog = './test_info.log'

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger(__name__, "INFO", True)

        pub.sendMessage('fail_delete_fmea',
                        error_message=("Attempted to delete non-existent "
                                       "FMEA "
                                       "element ID ax."))
        pub.sendMessage('fail_update_fmea',
                        error_message=("Attempted to save non-existent FMEA "
                                       "element with FMEA ID ax."))

        _test_log = open(_testlog, 'r')
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers['test_logger'], logging.Logger)
        assert _lines[0].split('-', 5)[-1].split(':', 1)[-1].strip() == (
            'Attempted to delete non-existent FMEA element ID ax.')
        assert _lines[1].split('-', 5)[-1].split(':', 1)[-1].strip() == (
            'Attempted to save non-existent FMEA element with FMEA ID ax.')

    @pytest.mark.unit
    def test_info_not_log_debug_messages(self):
        """do_log_info() should not log DEBUG level information when it is an INFO log manager."""
        _testlog = './test_info.log'

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger(__name__, "INFO")

        DUT.do_log_debug(
            __name__, "This is a test DEBUG level message that should not "
            "be logged.")

        _test_log = open(_testlog, 'r')
        _lines = _test_log.readlines()

        assert _lines == []

    @pytest.mark.unit
    def test_info_log_info_messages(self):
        """do_log_info() should log INFO level information when it is an INFO log manager."""
        _testlog = './test_info.log'

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger(__name__, "INFO")

        DUT.do_log_info(
            __name__, "This is a test INFO level message that should be "
            "logged.")

        _test_log = open(_testlog, 'r')
        _lines = _test_log.readlines()

        assert _lines[0].split('-', 5)[-1].split(':', 1)[-1].strip() == (
            'This is a test INFO level message that should be logged.')

    @pytest.mark.unit
    def test_info_log_higher_level_messages(self):
        """do_log_info() should log WARN, ERROR, and CRITICAL level information when it is an INFO log manager."""
        _testlog = './test_info.log'

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger(__name__, "INFO")

        DUT.do_log_warning(
            __name__, "This is a test WARN level message that should be "
            "logged.")
        DUT.do_log_error(
            __name__, "This is a test ERROR level message that should be "
            "logged.")
        DUT.do_log_critical(
            __name__, "This is a test CRITICAL level message that should "
            "be logged.")

        _test_log = open(_testlog, 'r')
        _lines = _test_log.readlines()

        assert _lines[0].split('-', 5)[-1].split(':', 1)[-1].strip() == (
            'This is a test WARN level message that should be logged.')
        assert _lines[1].split('-', 5)[-1].split(':', 1)[-1].strip() == (
            'This is a test ERROR level message that should be logged.')
        assert _lines[2].split('-', 5)[-1].split(':', 1)[-1].strip() == (
            'This is a test CRITICAL level message that should be logged.')
