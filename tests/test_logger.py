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


@pytest.fixture(scope="function")
def test_logger(test_log_file):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut).
    dut = RAMSTKLogManager(test_log_file)

    yield dut

    # Unsubscribe from pypubsub topics.
    assert pub.unsubscribe(dut.do_log_debug, "do_log_debug_msg")
    assert pub.unsubscribe(dut.do_log_info, "do_log_info_msg")
    assert pub.unsubscribe(dut.do_log_warning, "do_log_warning_msg")
    assert pub.unsubscribe(dut.do_log_error, "do_log_error_msg")
    assert pub.unsubscribe(dut.do_log_critical, "do_log_critical_msg")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_logger", "test_log_file")
class TestLogManager:
    """Test class for RAMSTKLogManager methods."""

    @pytest.mark.unit
    def test_create_log_manager(self, test_logger, test_log_file):
        """__init__() should create an instance of the RAMSTKLogManager."""
        assert isinstance(test_logger, RAMSTKLogManager)
        assert isinstance(test_logger.loggers, dict)
        assert test_logger.log_file == test_log_file
        assert pub.isSubscribed(test_logger.do_log_debug, "do_log_debug_msg")
        assert pub.isSubscribed(test_logger.do_log_info, "do_log_info_msg")
        assert pub.isSubscribed(test_logger.do_log_warning, "do_log_warning_msg")
        assert pub.isSubscribed(test_logger.do_log_error, "do_log_error_msg")
        assert pub.isSubscribed(test_logger.do_log_critical, "do_log_critical_msg")

    @pytest.mark.unit
    def test_do_log_debug(self, test_logger, test_log_file):
        """do_log_debug() should be called when the do_log_debug_msg message is
        broadcast and log the associated debug message."""
        test_logger.do_create_logger("DEBUG", "DEBUG", True)

        pub.sendMessage(
            "do_log_debug_msg",
            logger_name="DEBUG",
            message="Test DEBUG message sent and logged.",
        )

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["DEBUG"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test DEBUG message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_info(self, test_logger, test_log_file):
        """do_log_info() should be called when the do_log_info_msg message is broadcast
        and log the associated debug message."""
        test_logger.do_create_logger("INFO", "INFO", True)

        pub.sendMessage(
            "do_log_info_msg",
            logger_name="INFO",
            message="Test INFO message sent and logged.",
        )

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["INFO"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test INFO message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_info_ignore_debug(self, test_logger, test_log_file):
        """do_log_info() should not be called when the do_log_debug_msg message is
        broadcast and the log level is INFO."""
        test_logger.do_create_logger("INFO", "INFO", True)

        pub.sendMessage(
            "do_log_debug_msg",
            logger_name="INFO",
            message="Test DEBUG message sent and logged.",
        )

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["INFO"], logging.Logger)
        assert _lines == []

    @pytest.mark.unit
    def test_do_log_info_higher_level_messages(self, test_logger, test_log_file):
        """do_log_info() should log WARN, ERROR, and CRITICAL level information when it
        is an INFO log manager."""
        test_logger.do_create_logger("INFO", "INFO")

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

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["INFO"], logging.Logger)
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
    def test_do_log_warning(self, test_logger, test_log_file):
        """do_log_warning() should be called when the do_log_warning_msg message is
        broadcast and log the associated debug message."""
        test_logger.do_create_logger("WARN", "WARN", True)

        pub.sendMessage(
            "do_log_warning_msg",
            logger_name="WARN",
            message="Test WARN message sent and logged.",
        )

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["WARN"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test WARN message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_warning_ignore_debug_info(self, test_logger, test_log_file):
        """do_log_warning() should not log a debug or info message."""
        test_logger.do_create_logger("WARN", "WARN", True)

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

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["WARN"], logging.Logger)
        assert _lines == []

    @pytest.mark.unit
    def test_do_log_error(self, test_logger, test_log_file):
        """do_log_error() should be called when the do_log_error_msg message is
        broadcast and log the associated debug message."""
        test_logger.do_create_logger("ERROR", "ERROR", True)

        pub.sendMessage(
            "do_log_error_msg",
            logger_name="ERROR",
            message="Test ERROR message sent and logged.",
        )

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["ERROR"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test ERROR message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_error_ignore_debug_info_warning(self, test_logger, test_log_file):
        """do_log_warning() should not log a debug, info, or warning message."""
        test_logger.do_create_logger("ERROR", "ERROR", True)

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

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["ERROR"], logging.Logger)
        assert _lines == []

    @pytest.mark.unit
    def test_do_log_critical(self, test_logger, test_log_file):
        """do_log_critical() should be called when the do_log_critical_msg message is
        broadcast and log the associated debug message."""
        test_logger.do_create_logger("CRITICAL", "CRITICAL", True)

        pub.sendMessage(
            "do_log_critical_msg",
            logger_name="CRITICAL",
            message="Test CRITICAL message sent and logged.",
        )

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["CRITICAL"], logging.Logger)
        assert _lines[0].split(":", 5)[-1].strip() == (
            "Test CRITICAL message sent and logged."
        )

    @pytest.mark.unit
    def test_do_log_critical_ignore_debug_info_warning_error(
        self, test_logger, test_log_file
    ):
        """do_log_warning() should not log a debug, info, warning, or error message."""
        test_logger.do_create_logger("CRITICAL", "CRITICAL", True)

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

        _test_log = open(test_log_file, "r")
        _lines = _test_log.readlines()

        assert isinstance(test_logger.loggers["CRITICAL"], logging.Logger)
        assert _lines == []
