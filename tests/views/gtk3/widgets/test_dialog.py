# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_dialog.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 button module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import (
    RAMSTKDateSelect,
    RAMSTKDialog,
    RAMSTKFileChooser,
    RAMSTKMessageDialog,
)


class TestRAMSTKDateSelect:
    """Test class for the RAMSTKDateSelect."""

    @pytest.mark.gui
    def test_create_date_select(self):
        """__init__() should create a RAMSTKDialog."""
        DUT = RAMSTKDateSelect()

        assert isinstance(DUT, RAMSTKDateSelect)
        assert DUT.get_title() == "Select Date"


class TestRAMSTKDialog:
    """Test class for the RAMSTKDialog."""

    @pytest.mark.gui
    def test_create_dialog(self):
        """__init__() should create a RAMSTKDialog."""
        DUT = RAMSTKDialog("Test Dialog Title")

        assert isinstance(DUT, RAMSTKDialog)
        assert DUT.get_destroy_with_parent()
        assert DUT.get_modal()
        assert DUT.get_parent() is None
        assert DUT.get_title() == "Test Dialog Title"

    @pytest.mark.gui
    def test_destroy_dialog(self):
        """do_destroy() should return a when the dialog is run."""
        DUT = RAMSTKDialog("Test Dialog Title")

        assert DUT.do_destroy() is None


class TestRAMSTKFileChooser:
    """Test class for the RAMSTKFileChooser."""

    @pytest.mark.gui
    def test_create_file_chooser(self):
        """__init__() should create a RAMSTKFileChooser."""
        DUT = RAMSTKFileChooser("Test File Chooser Dialog", None)

        assert isinstance(DUT, RAMSTKFileChooser)
        assert DUT.get_destroy_with_parent()
        assert DUT.get_modal()
        assert DUT.get_parent() is None
        assert DUT.get_title() == "Test File Chooser Dialog"
        assert DUT.get_action() == Gtk.FileChooserAction.SAVE
        assert DUT.get_current_folder() is None


class TestRAMSTKMessageDialog:
    """Test class for the RAMSTKMessageDialog."""

    @pytest.mark.gui
    def test_create_error_message_dialog(self):
        """__init__() should create an error type RAMSTKMessageDialog."""
        DUT = RAMSTKMessageDialog()
        DUT.do_set_message("Test Prompt")
        DUT.do_set_message_type("error")

        assert isinstance(DUT, RAMSTKMessageDialog)
        assert DUT.get_destroy_with_parent()
        assert DUT.get_modal()
        assert DUT.get_parent() is None
        assert DUT.get_property("message-type") == Gtk.MessageType.ERROR
        assert DUT.get_property("text") == (
            "<b>Test Prompt  Check the error log for additional information "
            "(if any).  Please e-mail <span foreground='blue' "
            "underline='single'><a href='mailto:bugs@reliaqual.com?subject=RAMSTK BUG REPORT: "
            "<ADD SHORT PROBLEM DESCRIPTION>&amp;body=RAMSTK "
            "MODULE:%0d%0a%0d%0aRAMSTK VERSION:%20%0d%0a%0d%0aYOUR "
            "HARDWARE:%20%0d%0a%0d%0aYOUR OS:%20%0d%0a%0d%0aDETAILED PROBLEM DESCRIPTION:%20%0d%0a'>bugs@reliaqual.com</a></span> "
            "with a detailed description of the problem, the workflow you are "
            "using and the error log attached if the problem persists.</b>"
        )

    @pytest.mark.gui
    def test_create_warning_message_dialog(self):
        """__init__() should create a warning type RAMSTKMessageDialog."""
        DUT = RAMSTKMessageDialog()
        DUT.do_set_message("Test Warning Prompt")
        DUT.do_set_message_type("warning")

        assert isinstance(DUT, RAMSTKMessageDialog)
        assert DUT.get_destroy_with_parent()
        assert DUT.get_modal()
        assert DUT.get_parent() is None
        assert DUT.get_property("message-type") == Gtk.MessageType.WARNING
        assert DUT.get_property("text") == ("Test Warning Prompt")

    @pytest.mark.gui
    def test_create_info_message_dialog(self):
        """__init__() should create an info type RAMSTKMessageDialog."""
        DUT = RAMSTKMessageDialog()
        DUT.do_set_message("Test Info Prompt")
        DUT.do_set_message_type("information")

        assert isinstance(DUT, RAMSTKMessageDialog)
        assert DUT.get_destroy_with_parent()
        assert DUT.get_modal()
        assert DUT.get_parent() is None
        assert DUT.get_property("message-type") == Gtk.MessageType.INFO
        assert DUT.get_property("text") == ("Test Info Prompt")

    @pytest.mark.gui
    def test_create_question_message_dialog(self):
        """__init__() should create a question type RAMSTKMessageDialog."""
        DUT = RAMSTKMessageDialog()
        DUT.do_set_message("Test Question Prompt")
        DUT.do_set_message_type("question")

        assert isinstance(DUT, RAMSTKMessageDialog)
        assert DUT.get_destroy_with_parent()
        assert DUT.get_modal()
        assert DUT.get_parent() is None
        assert DUT.get_property("message-type") == Gtk.MessageType.QUESTION
        assert DUT.get_property("text") == ("Test Question Prompt")
