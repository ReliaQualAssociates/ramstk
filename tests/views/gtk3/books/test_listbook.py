# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.books.test_listbook.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 basebook list algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.books import RAMSTKListBook


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestRAMSTKListBook():
    """Test class for the RAMSTKBook."""
    @pytest.mark.gui
    def test_create_listbook(self, test_toml_user_configuration):
        """__init__() should create a RAMSTKListBook."""
        DUT = RAMSTKListBook(
            test_toml_user_configuration,
            RAMSTKLogManager(test_toml_user_configuration.RAMSTK_USER_LOG))

        assert isinstance(DUT, RAMSTKListBook)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert DUT.dic_tab_position['left'] == Gtk.PositionType.LEFT
        assert DUT.dic_tab_position['right'] == Gtk.PositionType.RIGHT
        assert DUT.dic_tab_position['top'] == Gtk.PositionType.TOP
        assert DUT.dic_tab_position['bottom'] == Gtk.PositionType.BOTTOM
        assert isinstance(DUT._dic_list_views, dict)
        assert pub.isSubscribed(DUT._on_module_change, 'mvwSwitchedPage')
        assert pub.isSubscribed(DUT._on_close, 'succeed_closed_program')
