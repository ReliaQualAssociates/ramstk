# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.test_utilities.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Utilities module algorithms and models."""

# Standard Library Imports
import logging
import os

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk import RAMSTKLogManager


class TestLogManager:
    """Test class for RAMSTKLogManager methods."""

    def test_create_log_manager(self):
        """__init__() should create an instance of the RAMSTKLogManager."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)

        assert isinstance(DUT, RAMSTKLogManager)
        assert isinstance(DUT.loggers["ramstk.logger"], logging.Logger)
        assert DUT.log_file == _testlog
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_delete_fmea")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_action")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_cause")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_control")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_mechanism")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_mode")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_update_fmea")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_delete_function")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_delete_hazard")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_function")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_hazard")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_update_function")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_hardware")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_validation")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_stakeholder")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_revision")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_environment")
        assert pub.isSubscribed(
            DUT._do_log_fail_message, "fail_insert_failure_definition"
        )
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_mission")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_mission_phase")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_requirement")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_opload")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_opstress")
        assert pub.isSubscribed(DUT._do_log_fail_message, "fail_insert_test_method")

    @pytest.mark.unit
    def test_log_fail_messages(self):
        """_do_log_fail_message() should be called when fail_* messages are broadcast and log the associated error message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("DEBUG", "DEBUG", True)

        pub.sendMessage(
            "fail_delete_fmea",
            error_message=("Attempted to delete non-existent " "FMEA element ID ax."),
        )
        pub.sendMessage(
            "fail_update_fmea",
            error_message=(
                "Attempted to save non-existent FMEA " "element with FMEA ID ax."
            ),
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["DEBUG"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Attempted to delete non-existent FMEA element ID ax."
        )
        assert _lines[1].split(":", 5)[-1].strip() == (
            "Attempted to save non-existent FMEA element with FMEA ID ax."
        )

    @pytest.mark.unit
    def test_do_log_debug(self):
        """do_log_debug() should be called when the do_log_debug_msg message is broadcast and log the associated debug message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("DEBUG", "DEBUG", True)

        pub.sendMessage(
            "do_log_debug_msg",
            logger_name="DEBUG",
            message="Test DEBUG message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["DEBUG"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test DEBUG message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_info(self):
        """do_log_info() should be called when the do_log_info_msg message is broadcast and log the associated debug message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("INFO", "INFO", True)

        pub.sendMessage(
            "do_log_info_msg",
            logger_name="INFO",
            message="Test INFO message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["INFO"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test INFO message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_info_ignore_debug(self):
        """do_log_info() should not be called when the do_log_debug_msg message is broadcast and the log level is INFO."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("INFO", "INFO", True)

        pub.sendMessage(
            "do_log_debug_msg",
            logger_name="INFO",
            message="Test DEBUG message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["INFO"], logging.Logger)
        assert _lines == []

    @pytest.mark.unit
    def test_do_log_info_higher_level_messages(self):
        """do_log_info() should log WARN, ERROR, and CRITICAL level information when it is an INFO log manager."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("INFO", "INFO")

        pub.sendMessage(
            "do_log_warning_msg",
            logger_name="INFO",
            message="Test WARN message sent and logged.",
        )
        pub.sendMessage(
            "do_log_error_msg",
            logger_name="INFO",
            message="Test ERROR message sent and logged.",
        )
        pub.sendMessage(
            "do_log_critical_msg",
            logger_name="INFO",
            message="Test CRITICAL message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["INFO"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test WARN message sent and logged."
        )
        assert _lines[1].split(":", 5)[-1].strip() == (
            "Test ERROR message sent and logged."
        )
        assert _lines[2].split(":", 5)[-1].strip() == (
            "Test CRITICAL message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_warning(self):
        """do_log_warning() should be called when the do_log_warning_msg message is broadcast and log the associated debug message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("WARN", "WARN", True)

        pub.sendMessage(
            "do_log_warning_msg",
            logger_name="WARN",
            message="Test WARN message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["WARN"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test WARN message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_warning_ignore_debug_info(self):
        """do_log_warning() should not log a debug or info message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("WARN", "WARN", True)

        pub.sendMessage(
            "do_log_debug_msg",
            logger_name="WARN",
            message="Test DEBUG message sent and logged.",
        )
        pub.sendMessage(
            "do_log_info_msg",
            logger_name="WARN",
            message="Test INFO message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["WARN"], logging.Logger)
        assert _lines == []

    @pytest.mark.unit
    def test_do_log_error(self):
        """do_log_error() should be called when the do_log_error_msg message is broadcast and log the associated debug message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("ERROR", "ERROR", True)

        pub.sendMessage(
            "do_log_error_msg",
            logger_name="ERROR",
            message="Test ERROR message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["ERROR"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test ERROR message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_error_ignore_debug_info_warning(self):
        """do_log_warning() should not log a debug, info, or warning message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("ERROR", "ERROR", True)

        pub.sendMessage(
            "do_log_debug_msg",
            logger_name="ERROR",
            message="Test DEBUG message sent and logged.",
        )
        pub.sendMessage(
            "do_log_info_msg",
            logger_name="ERROR",
            message="Test INFO message sent and logged.",
        )
        pub.sendMessage(
            "do_log_warning_msg",
            logger_name="ERROR",
            message="Test WARN message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["ERROR"], logging.Logger)
        assert _lines == []

    @pytest.mark.unit
    def test_do_log_critical(self):
        """do_log_critical() should be called when the do_log_critical_msg message is broadcast and log the associated debug message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("CRITICAL", "CRITICAL", True)

        pub.sendMessage(
            "do_log_critical_msg",
            logger_name="CRITICAL",
            message="Test CRITICAL message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["CRITICAL"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test CRITICAL message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_critical_ignore_debug_info_warning_error(self):
        """do_log_warning() should not log a debug, info, warning, or error message."""
        _testlog = "./test_info.log"
        if os.path.exists(_testlog):
            os.remove(_testlog)

        DUT = RAMSTKLogManager(_testlog)
        DUT.do_create_logger("CRITICAL", "CRITICAL", True)

        pub.sendMessage(
            "do_log_debug_msg",
            logger_name="CRITICAL",
            message="Test DEBUG message sent and logged.",
        )
        pub.sendMessage(
            "do_log_info_msg",
            logger_name="CRITICAL",
            message="Test INFO message sent and logged.",
        )
        pub.sendMessage(
            "do_log_warning_msg",
            logger_name="CRITICAL",
            message="Test WARN message sent and logged.",
        )
        pub.sendMessage(
            "do_log_error_msg",
            logger_name="CRITICAL",
            message="Test ERROR message sent and logged.",
        )

        _test_log = open(_testlog, "r")
        _lines = _test_log.readlines()

        assert isinstance(DUT.loggers["CRITICAL"], logging.Logger)
        assert _lines == []
