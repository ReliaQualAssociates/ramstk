# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_scrolledwindow.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for the GTK3 scrolledwindow module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import RAMSTKScrolledWindow


class TestRAMSTKScrolledWindow():
    """Test class for the RAMSTKScrolledWindow."""
    @pytest.mark.gui
    def test_create_scrolledwindow_viewport(self):
        """__init__() should create a RAMSTKScrolledWindow."""
        DUT = RAMSTKScrolledWindow(Gtk.Fixed())

        assert isinstance(DUT, RAMSTKScrolledWindow)
        assert DUT.get_property(
            'hscrollbar-policy') == Gtk.PolicyType.AUTOMATIC
        assert DUT.get_property(
            'vscrollbar-policy') == Gtk.PolicyType.AUTOMATIC
