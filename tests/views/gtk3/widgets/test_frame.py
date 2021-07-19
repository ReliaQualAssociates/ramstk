# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_frame.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 entry module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import RAMSTKFrame


class TestRAMSTKFrame:
    """Test class for the RAMSTKFrame."""

    @pytest.mark.gui
    def test_create_frame(self):
        """__init__() should create a RAMSTKFrame."""
        DUT = RAMSTKFrame()

        assert isinstance(DUT, RAMSTKFrame)
        assert DUT.get_property("height-request") == -1
        assert DUT.get_property("width-request") == -1

    @pytest.mark.gui
    def test_set_properties(self):
        """do_set_properties() should set the properties of a RAMSTKEntry."""
        DUT = RAMSTKFrame()
        DUT.do_set_properties(title="Test Frame Title", shadow=Gtk.ShadowType.ETCHED_IN)

        assert DUT.get_property("label") == "Test Frame Title"
        assert DUT.get_property("shadow-type") == Gtk.ShadowType.ETCHED_IN

    @pytest.mark.gui
    def test_set_properties_default_values(self):
        """do_set_properties() should set the default properties of a RAMSTKFrame when no keywords are passed to the method."""
        DUT = RAMSTKFrame()
        DUT.do_set_properties()

        assert DUT.get_property("label") == ""
        assert DUT.get_property("shadow-type") == Gtk.ShadowType.ETCHED_OUT
