# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.books.test_modulebook.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 basebook module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.books import RAMSTKModuleBook


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestRAMSTKModuleBook():
    """Test class for the RAMSTKBook."""
    @pytest.mark.gui
    def test_create_modulebook(self, test_toml_user_configuration):
        """__init__() should create a RAMSTKModuleBook."""
        DUT = RAMSTKModuleBook(
            test_toml_user_configuration,
            RAMSTKLogManager(test_toml_user_configuration.RAMSTK_USER_LOG))

        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert DUT.dic_tab_position['left'] == Gtk.PositionType.LEFT
        assert DUT.dic_tab_position['right'] == Gtk.PositionType.RIGHT
        assert DUT.dic_tab_position['top'] == Gtk.PositionType.TOP
        assert DUT.dic_tab_position['bottom'] == Gtk.PositionType.BOTTOM
        assert isinstance(DUT, RAMSTKModuleBook)
        assert isinstance(DUT._dic_module_views, dict)
        assert pub.isSubscribed(DUT._on_open, 'succeed_retrieve_revisions')
        assert pub.isSubscribed(DUT._on_close, 'succeed_closed_program')
