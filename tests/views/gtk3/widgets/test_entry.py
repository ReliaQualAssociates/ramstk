# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_entry.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 entry module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import RAMSTKEntry, RAMSTKTextView


class TestRAMSTKEntry():
    """Test class for the RAMSTKEntry."""
    @pytest.mark.gui
    def test_create_entry(self):
        """__init__() should create a RAMSTKCEntry."""
        DUT = RAMSTKEntry()

        assert isinstance(DUT, RAMSTKEntry)
        assert DUT.get_property('height-request') == -1
        assert DUT.get_property('width-request') == -1

    @pytest.mark.gui
    def test_set_properties(self):
        """do_set_properties() should set the properties of a RAMSTKEntry."""
        DUT = RAMSTKEntry()
        DUT.do_set_properties(height=70,
                              width=150,
                              editable=False,
                              tooltip="Test Entry Tooltip.")

        assert not DUT.get_property('editable')
        assert DUT.get_property('height-request') == 70
        assert DUT.get_property('width-request') == 150
        assert DUT.get_property('tooltip-markup') == "Test Entry Tooltip."

    @pytest.mark.gui
    def test_set_properties_default_values(self):
        """do_set_properties() should set the default properties of a RAMSTKButton when no keywords are passed to the method."""
        DUT = RAMSTKEntry()
        DUT.do_set_properties()

        assert DUT.get_property('height-request') == 25
        assert DUT.get_property('tooltip-markup') == (
            "Missing tooltip, please file a quality type issue to have one "
            "added.")
        assert DUT.get_property('width-request') == 200

    @pytest.mark.gui
    def test_set_properties_zero_height(self):
        """do_set_properties() should set the height to the default value if it is passed as zero."""
        DUT = RAMSTKEntry()
        DUT.do_set_properties(height=0)

        assert DUT.get_property('height-request') == 25

    @pytest.mark.gui
    def test_set_properties_zero_width(self):
        """do_set_properties() should set the width to the default value if it is passed as zero."""
        DUT = RAMSTKEntry()
        DUT.do_set_properties(width=0)

        assert DUT.get_property('width-request') == 200


class TestRAMSTKTextView():
    """Test class for the RAMSTKTextView."""
    @pytest.mark.gui
    def test_create_text_view(self):
        """__init__() should create a RAMSTKTextView."""
        DUT = RAMSTKTextView(Gtk.TextBuffer())

        assert isinstance(DUT, RAMSTKTextView)
        assert DUT.get_property('height-request') == -1
        assert DUT.get_property('width-request') == -1

    @pytest.mark.gui
    def test_set_properties_default_values(self):
        """do_set_properties() should set the default properties of a RAMSTKButton when no keywords are passed to the method."""
        DUT = RAMSTKTextView(Gtk.TextBuffer())
        DUT.do_set_properties()

        assert DUT.scrollwindow.get_property('height-request') == 100
        assert DUT.get_property('tooltip-markup') == (
            "Missing tooltip, please file a quality type issue to have one "
            "added.")
        assert DUT.scrollwindow.get_property('width-request') == 200

    @pytest.mark.gui
    def test_set_properties_zero_height(self):
        """do_set_properties() should set the height to the default value if it is passed as zero."""
        DUT = RAMSTKTextView(Gtk.TextBuffer())
        DUT.do_set_properties(height=0)

        assert DUT.scrollwindow.get_property('height-request') == 100

    @pytest.mark.gui
    def test_set_properties_zero_width(self):
        """do_set_properties() should set the width to the default value if it is passed as zero."""
        DUT = RAMSTKTextView(Gtk.TextBuffer())
        DUT.do_set_properties(width=0)

        assert DUT.scrollwindow.get_property('width-request') == 200
