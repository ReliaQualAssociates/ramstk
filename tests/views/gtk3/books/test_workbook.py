# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.books.test_workbook.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 basebook work algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.books import RAMSTKWorkBook


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestRAMSTKWorkBook():
    """Test class for the RAMSTKBook."""
    @pytest.mark.gui
    def test_create_workbook(self, test_toml_user_configuration):
        """__init__() should create a RAMSTKWorkBook."""
        DUT = RAMSTKWorkBook(
            test_toml_user_configuration,
            RAMSTKLogManager(test_toml_user_configuration.RAMSTK_USER_LOG))

        # Did it inherit from the RAMSTKBook?
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert DUT.dic_tab_position['left'] == Gtk.PositionType.LEFT
        assert DUT.dic_tab_position['right'] == Gtk.PositionType.RIGHT
        assert DUT.dic_tab_position['top'] == Gtk.PositionType.TOP
        assert DUT.dic_tab_position['bottom'] == Gtk.PositionType.BOTTOM
        assert isinstance(DUT, RAMSTKWorkBook)
        assert isinstance(DUT.dic_work_views, dict)
        assert pub.isSubscribed(DUT._on_module_change, 'mvwSwitchedPage')
